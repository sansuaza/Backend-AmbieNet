"""post sealizer"""
#Django
from django.core import mail

#Django REST Framework
from rest_framework import serializers

#Models
from AmbieNet.posts.models import Post, Validator
from AmbieNet.users.models import User

class ValidatorModelSerializer(serializers.ModelSerializer):

    
    class Meta:
        """Meta Class"""
        model = Validator
        
        fields = (
            'user',
            'post',
        )


class ValidatorCreateSerializer(serializers.Serializer):

    user = serializers.CharField(
        min_length = 1,
        max_length = 50
    )

    post = serializers.CharField(
        min_length = 1,
        max_length = 50
    )

    def create(self, data):
        #Modificar esta busqueda manual, esto se debe sacar por el self, no entiendo porque pero asi dice don suaza :D
        import pdb; pdb.set_trace()
        print("llega hasta el create de serializer-------------------------")
        user = User.objects.get(username=data['user'])
        post = Post.objects.get(id=data['post'])
        data['user']=user
        data['post']=post
        validator = Validator.objects.create(**data)
       
        return validator

    #def validate(self,data):
        