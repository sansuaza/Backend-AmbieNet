
#Django REST Framework
from rest_framework import serializers

#Django
from django.forms import ImageField

#Models
from AmbieNet.posts.models import Post, Image




class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta Class"""
        model = Post
        fields = (
            'post',
            'image'
        )

class ImageCreateSerializer(serializers.Serializer):

    image = ImageField(max_length=None, allow_empty_file=False)

    post = serializers.CharField(min_length = 5)

    def create (self,data):
        post = Post.objects.get(id=data['post'])
        data.pop('post')
        image = Image.objects.create(post=post,**data)

