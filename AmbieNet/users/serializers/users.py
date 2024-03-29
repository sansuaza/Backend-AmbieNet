"""user sealizer"""
#Django
from django.contrib.auth import  authenticate
from django.core.validators import RegexValidator

#Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

#Models
from AmbieNet.users.models import User,Profile

#Serializers
from AmbieNet.users.serializers.profiles import ProfileModelSerializer

class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)
    class Meta:
        """Meta class"""
        model = User
        fields = (
            'username',
            'is_active',
            'level',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_staff',
            'role',
            'profile'
        )

        read_only_fields = (
            'role',
        )

    def validate(self, data):
        is_staff_field = data.get('is_staff', None)
        if is_staff_field != None:
            raise serializers.ValidationError('is_staff field can not be modified.')

        return data


class UserSignUpSerializer(serializers.Serializer):

    username = serializers.CharField(
        min_length = 6,
        max_length = 20,
        validators = [UniqueValidator(queryset=User.objects.all())]
        )

    email = serializers.EmailField(
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    phone_regex = RegexValidator(

        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )

    phone_number = serializers.CharField(validators= [phone_regex])

    password = serializers.CharField(
        min_length=6,
        max_length=16
    )

    first_name = serializers.CharField(min_length=3, max_length=20)
    last_name = serializers.CharField(min_length=3, max_length=20)

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def create(self, data):

        data_profile = {}
        data_profile['latitude'] = data['latitude']
        data_profile['longitude'] = data['longitude']

        data.pop('latitude')
        data.pop('longitude')

        user= User.objects.create_user(**data, is_verified=True)
        profile = Profile.objects.create(user=user, **data_profile)
        return user

class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""
    username = serializers.CharField()

    password = serializers.CharField(min_length= 4, max_length = 64)

    def validate (self, data):

        user = authenticate(username= data['username'], password = data['password'])

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        self.context['user']= user
        return data

    def create(self, data):
        """Generate or retrive new token."""

        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
