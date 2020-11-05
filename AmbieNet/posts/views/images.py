#Django rest freamwork
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

#Models
from AmbieNet.posts.models import Post,Image

#Serialzers
from AmbieNet.posts.serializers import(
    ImageModelSerializer,
    ImageCreateSerializer
)

class ImageCreateApiView(APIView):
 
    def post(self,request, *args, **kwargs):
        serializer = ImageCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.save()
        data = ImageModelSerializer(image).data
        return Response(data, status = status.HTTP_201_CREATED)