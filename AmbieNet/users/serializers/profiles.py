"""Profile serializer."""

#Django REST Framework
from rest_framework import serializers

#Models
from AmbieNet.users.models import Profile
    


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = (
            'biography',
            'country',
            'state',
            'city',
            'reputation'
        )
        read_only_fields=(
            'reputation',
        )
