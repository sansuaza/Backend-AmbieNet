"""post sealizer"""

#Django REST Framework
from rest_framework import serializers

#Models
from AmbieNet.posts.models import Post, Image
#from AmbieNet.users.models import User, Profile

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta Class"""
        model = Post
        fields = (
            'user_id',
            'profile_id',
            'title',
            'description',
            'type_catastrophe',
            'latitud',
            'longitud',
            #'photo'
        )

class PostCreateSerializer(serializers.Serializer):

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

    latitud = serializers.FloatField()
    longitud = serializers.FloatField()


 
    def create(self, data):
        
        post = Post.objects.create(**data)
        return post