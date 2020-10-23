"""Posts views"""

#Django rest freamwork
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

#Models
from AmbieNet.posts.models import Post,Image
from AmbieNet.users.models import User

#Serialzers
from AmbieNet.posts.serializers import(
    PostModelSerializer,
    PostCreateSerializer
)

class PostCreateApiView(APIView):
    def post(self,request, *args, **kwargs):
        serializer = PostCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        data = PostModelSerializer(post).data
        return Response(data, status = status.HTTP_201_CREATED)