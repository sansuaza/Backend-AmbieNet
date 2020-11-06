
#Django REST Framework
from rest_framework import serializers

#Django
from django.forms import ImageField

#Models
from AmbieNet.posts.models import Post, Image




class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta Class"""
        model = Image
        fields = (
            'post',
            'photo'
        )

class ImageCreateSerializer(serializers.Serializer):

    post = serializers.CharField(min_length = 1)
    
    photo = ImageField(max_length=None, allow_empty_file=False)

    def create (self,data):
        post = Post.objects.get(id=data['post'])
        data.pop('post')
        image = Image.objects.create(post=post,**data)
        return image

