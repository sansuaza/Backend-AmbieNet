"""post sealizer"""

#Django REST Framework
from rest_framework import serializers

#Models
from AmbieNet.posts.models import Post
from AmbieNet.users.models import User, Profile

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta Class"""
        model = Post
        fields = (
            'user',
            'title',
            'description',
            'type_catastrophe',
            'latitude',
            'longitude',
            'photo',
            'validator_number',
        )

        read_only_fields = (
            'user',
            'title',
            'latitud',
            'longitud',
            'photo',
            'type_catastrophe',
        )

class PostCreateSerializer(serializers.Serializer):

    """ user = serializers.PrimaryKeyRelatedField(many=True, read_only=True) """

     
    """
    profile = serializers.CharField(
        min_length = 1,
        max_length = 50
    ) """

    user = serializers.CharField(
        min_length = 1,
        max_length = 50
    )

    photo = serializers.CharField(
        max_length = 255
    )

    title = serializers.CharField(
        min_length = 5,
        max_length = 50
    )

    description = serializers.CharField(
        min_length = 5,
        max_length = 255
    )

    type_catastrophe = serializers.CharField (
        min_length = 2,
        max_length = 20
    )

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    


 
    def create(self, data):
        #Modificar esta busqueda manual, esto se debe sacar por el self, no entiendo porque pero asi dice don suaza :D
        user = User.objects.get(username=data['user'])
        profile = Profile.objects.get(user=user)
        data.pop('user')
        post = Post.objects.create(user=user, profile=profile,**data)
        return post



