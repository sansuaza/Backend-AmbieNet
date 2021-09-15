"""Admin views."""

# Django rest framework
from rest_framework.decorators import action
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

#Models
from AmbieNet.users.models import User, RoleRequest

# Permissions
from AmbieNet.users.permissions import IsAdminUser

# Serializers
from AmbieNet.users.serializers import (
    UserModelSerializer,
    RoleRequestModelSerializer,
    AnswerRoleRequestSerializer
)

class AdminViewSet(viewsets.GenericViewSet):

    def get_permissions(self):
        """Assign the permissions based on action required."""
        permissions = [IsAdminUser]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def pending_role_requests(self, request):
        """ query to get the pending role requests."""
        role_requests = RoleRequest.objects.filter(status=1)
        data = {
            'peding_role_requests' : RoleRequestModelSerializer(role_requests, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def change_role(self, request):
        """Handle of change de role from a user petition"""
        staff = request.user
        user = User.objects.get(username = request.data['username'])
        user.role = request.data['new_role']
        user.save()
        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def answer_role_requests(self, request):
        """Endpoint to the staff answer the role requests
        asked by the users."""

        user = User.objects.get(username = request.data['user__username'])
        new_role = 0
        if request.data['request_status'] == 'approved':
            new_role = request.data['new_role']

        serializer_data = {
            'staff_username' : request.user.username,
            'username' : user.username,
            'request_status' : request.data['request_status'],
            'new_role' : new_role
        }

        serializer = AnswerRoleRequestSerializer(data = serializer_data)
        serializer.is_valid(raise_exception = True)
        data = RoleRequestModelSerializer(serializer.save()).data

        return Response(data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def ban_users(self, request):
        """ Endpoint to bann an user. """
        user = User.objects.get(username = request.data['username'])

        if not user.is_active:
            return Response({"message": "user is already banned"}, status = status.HTTP_400_BAD_REQUEST)

        user.is_active = False
        user.save()
        data = UserModelSerializer(user).data

        return Response(data, status= status.HTTP_200_OK)