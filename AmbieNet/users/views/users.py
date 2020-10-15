"""Users views."""

# Django rest framework
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response

#Models
from AmbieNet.users.models import User,Profile

#Serializers
from AmbieNet.users.serializers import (
    UserModelSerializer, 
    UserLoginSerializer,
    UserSignUpSerializer
)

class UserViewSet(viewsets.GenericViewSet):
    """View sets"""
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data

        return Response(data, status = status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception= True)
        user, token = serializer.save()
        data = {
            'user' :  UserModelSerializer(user).data,
            'token' : token
        }
        return Response(data, status=status.HTTP_201_CREATED)




