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
    RoleRequestModelSerializer
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
