"""Posts views"""

#Django rest freamwork

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

#Models
from AmbieNet.posts.models import Post
from AmbieNet.users.models import User,Profile

#Permissions
from AmbieNet.posts.permissions import IsAdminUser

#Serialzers
from AmbieNet.posts.serializers import(
    PostModelSerializer,
    PostCreateSerializer
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
        if self.action in ['delete']:
            permissions = [isAdmin]
        return [permissions() for permission in permissions]
        

    def get_serializer_class(self):
        if (self.action in ['list', 'update']):
            return PostModelSerializer
        return PostCreateSerializer    


    @action(detail=False, methods=['post'])
    def postear(self,request, *args, **kwargs):
        """Handle of create the posts."""
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        data = PostModelSerializer(post).data
        return Response(data, status = status.HTTP_201_CREATED)


