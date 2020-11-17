"""Posts views"""

#Django rest freamwork

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated


#Models
from AmbieNet.posts.models import Post
from AmbieNet.users.models import User


#Serialzers
from AmbieNet.posts.serializers import(
    PostModelSerializer,
    PostCreateSerializer,
    ValidatorModelSerializer,
    ValidatorCreateSerializer
)

class PostViewSet(mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    
    queryset = Post.objects.all()
    lookup_field = 'id'

    def get_permissions(self):
        """Assign the permissions based on action required."""
        permissions = []
        if self.action in ['delete', 'destroy']:
            permissions = [IsAdminUser]
        return [permission() for permission in permissions]
        

    def get_serializer_class(self):
        if (self.action in ['list', 'update']):
            return PostModelSerializer
        return PostCreateSerializer    

    @action(detail=True, methods=['post'])
    def validator(self,request,*args,**kwargs):
        post=self.get_object()
        context = self.get_serializer_context()
        context['post'] = post
        serializer = ValidatorModelSerializer(data = request.data, context=context)
        serializer.is_valid(raise_expetion=True)
        data = serializer.save().data
        validators = Post.objects.get(data['post']).validator_number
        data['validator_number']=validators
        return Response(data, status = status.HTTP_201_CREATED)



    @action(detail=False, methods=['post'])
    def publicacion(self,request, *args, **kwargs):
        """Handle of create the posts."""
        
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data = request.data)
        
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        
        data = PostModelSerializer(post).data
        
        username = User.objects.get(id = data['user']).username
        data['user']= username
        return Response(data, status = status.HTTP_201_CREATED)


