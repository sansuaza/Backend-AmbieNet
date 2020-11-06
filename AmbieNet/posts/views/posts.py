"""Posts views"""

#Django rest freamwork

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

#Models
from AmbieNet.posts.models import Post
from AmbieNet.users.models import User

#Serialzers
from AmbieNet.posts.serializers import(
    PostModelSerializer,
    PostCreateSerializer
)

class PostViewSet(mixins.UpdateModelMixin,
                mixins.ListModelMixin
                ,viewsets.GenericViewSet):
    
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if (self.action == 'list'):
            return PostModelSerializer
        return PostCreateSerializer    

    @action(detail=False, methods=['post'])
    def postear(self,request, *args, **kwargs):
        serializer_class = get_serializer_class()
        serializer = serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        data = PostModelSerializer(post).data
        return Response(data, status = status.HTTP_201_CREATED)
