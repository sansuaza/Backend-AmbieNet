"""post sealizer"""

#Django REST Framework
from rest_framework import serializers

#Models
from AmbieNet.posts.models import Post, Image
from AmbieNet.users.models import User, Profile
#from AmbieNet.users.models import User, Profile

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta Class"""
        model = Post
        fields = (
            'user',
            'title',
            'description',
            'type_catastrophe',
            'latitud',
            'longitud',
            #'photo'
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
        #Modificar esta busqueda manual, esto se debe sacar por el self, no entiendo porque pero asi dice don suaza :D
        user = User.objects.get(username=data['user'])
        profile = Profile.objects.get(user=user)
        data.pop('user')
        post = Post.objects.create(user=user, profile=profile,**data)
        return post