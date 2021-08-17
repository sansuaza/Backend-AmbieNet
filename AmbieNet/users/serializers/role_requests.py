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

class RoleRequestModelSerializer(serializers.ModelSerializer):

    requesting_user = UserModelSerializer(read_only=True)
    class Meta:
        model = RoleRequest
        fields = ('new_role', 'message', 'requesting_user', 'status')

        read_only_fields = (
            'new_role',
            'message',
            'requesting_user',
            'status'
        )

class AnswerRoleRequestSerializer(serializers.Serializer):

    staff_username = serializers.CharField(min_length=6)
    username = serializers.CharField(min_length=6)
    request_status = serializers.CharField()
    new_role = serializers.IntegerField()

    def validate(self, data):
        """Handle of validate the existence of user role request."""
        user = User.objects.get(username = data['username'])
        user_requests = RoleRequest.objects.filter(
            requesting_user = user
        )

        if user_requests.exists():
            if user_requests.last().status != 1:
                raise serializers.ValidationError('This request has been answered in the past')
        else:
            raise serializers.ValidationError('This user doesn`t have pending requests')

        self.context['user_request'] = user_requests.last()
        self.context['requesting_user'] = user
        self.context['request_status'] = data['request_status']
        self.context['new_role'] = data['new_role']
        self.context['staff_username'] = data['staff_username']

        return data

    def save(self):

        role_request = self.context['user_request']
        requesting_user = self.context['requesting_user']

        if self.context['request_status'] == 'approved':
            role_request.status = '3'
            requesting_user.role = self.context['new_role']

            requesting_user.save()
        else:
            role_request.status = '2'

        role_request.staff_validator_username = self.context['staff_username']
        role_request.save()

        return role_request
