"""Users views."""

# Django rest framework
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

#Models
from AmbieNet.users.models import User,Profile, RoleRequest

#Permissions
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated
)
from AmbieNet.users.permissions import IsAccountOwner, IsAdminUser

#Serializers
from AmbieNet.users.serializers import (
    UserModelSerializer,
    UserLoginSerializer,
    UserSignUpSerializer,
    ProfileModelSerializer,
    CreateRoleRequestSerializer
)

class UserViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """cuando se redirecciona a este viewset, pide que haya autenticacion"""
    queryset = User.objects.exclude(is_staff=True)

    "lookup field is the atribute that will be used to search the user"
    lookup_field = "username"

    def get_serializer_class(self):
        """Assing the necessary serializer for each process."""
        if self.action == 'signup':
            return UserSignUpSerializer
        if self.action == 'login':
            return UserLoginSerializer
        if self.action in ['update', 'partial_update', 'retrieve', 'list']:
            return UserModelSerializer
        if self.action in ['make_request']:
            return CreateRoleRequestSerializer

    def get_permissions(self):
        """Assign the permissions based on action required."""
        permissions = []
        if self.action in ['signup', 'login']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAccountOwner]
        elif self.action in ['make_request']:
            permissions = [IsAuthenticated]
        elif self.action in ['list']:
            permissions = [IsAdminUser]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def make_request(self, request):
        serializer_class = self.get_serializer_class()
        data = request.data
        context = {}
        context['requesting_user_username'] = request.user.username
        serializer = serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data['user'] = context['requesting_user_username']
        return Response(data, status = status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data

        return Response(data, status = status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        data = {
            'user' :  UserModelSerializer(user).data,
            'token' : token
        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """ Update profile data. """
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)
