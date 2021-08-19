"""Posts views"""

#Django rest freamwork

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

#Models
from AmbieNet.posts.models import Post
from AmbieNet.users.models import User

#Serialzers
from AmbieNet.posts.serializers import(
    PostModelSerializer,
    PostCreateSerializer,
    ValidatorCreateSerializer
)

#Permissions
from AmbieNet.posts.permissions import IsPostOwner

class PostViewSet(mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):

    queryset = Post.objects.all()
    lookup_field = 'id'

    def get_permissions(self):
        """ Assign the permissions based on action required. """
        if self.action in ['list']:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        if self.action in ['delete', 'destroy']:
            permissions = [IsPostOwner | IsAdminUser]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """ Assing the necessary serializer for each process. """
        if (self.action in ['list', 'partial_update']):
            return PostModelSerializer
        return PostCreateSerializer

    @action(detail=False, methods=['post'])
    def validator(self,request,*args,**kwargs):
        """ Handle of validate the users by a user. """
        user = User.objects.get(username=request.data['user']).id
        post = Post.objects.get(id=request.data['post'])
        id_post=post.id
        datos = {
            'user' : user,
            'post' : id_post
        }
        serializer = ValidatorCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        validator = serializer.save()
        data = ValidatorCreateSerializer(validator).data
        #import pdb; pdb.set_trace()
        data['validator_number']=post.validator_number
        return Response(data, status = status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def publicacion(self,request, *args, **kwargs):
        """ Handle of create the posts. """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        data = PostModelSerializer(post).data

        return Response(data, status = status.HTTP_201_CREATED)
