"""Role request serializers."""
# Utils
import datetime

# Django REST Framework
from rest_framework import serializers

# Models
from AmbieNet.users.models import RoleRequest, User

# Serializers
from AmbieNet.users.serializers import UserModelSerializer

class CreateRoleRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleRequest
        fields = ('new_role', 'message')

    def validate(self, data):
        user = User.objects.get(username = self.context['requesting_user_username'])
        user_requests = RoleRequest.objects.filter(
            requesting_user = user
        )

        if user_requests.exists():
            last_user_request = user_requests.last()
            past_days = datetime.date.today().day - last_user_request.created.day

            if past_days < 30:
                raise serializers.ValidationError('This user have been done a request in the last 30 days')

        return data

    def create(self, data):
        user = User.objects.get(username = self.context['requesting_user_username'])
        role_request = RoleRequest.objects.create(
            requesting_user = user,
            **data
        )

        return role_request
