"""post sealizer"""
#Django
from django.core import mail

#Django REST Framework
from rest_framework import serializers

#Models
from AmbieNet.posts.models import Post
from AmbieNet.users.models import User

class ValidatorModelSerializer(serializers.ModelSerializer):

    
    class Meta:
        """Meta Class"""
        model = Post
        
        fields = (
            'user',
            'post',
        )


class ValidatorCreateSerializer(serializers.Serializer):

    post = serializers.CharField(
        min_length = 1,
        max_length = 50
    )

    def create(self, data):
        #Modificar esta busqueda manual, esto se debe sacar por el self, no entiendo porque pero asi dice don suaza :D
    
        post = Post.objects.get(id=data['post'])
        validator = Validator.objects.create(user=self.request.user, post=post ,**data)
       
        return validator

    #def validate(self,data):
        