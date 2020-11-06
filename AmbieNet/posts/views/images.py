#Django rest freamwork
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

#Models
from AmbieNet.posts.models import Image

#Serialzers
from AmbieNet.posts.serializers import(
    ImageModelSerializer,
    ImageCreateSerializer
)

class ImageViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    """Image viewset."""

    def get_serializer_class(self, request):
        """define the serializer that will be used"""
        if( self.action == 'create' ):
            return ImageCreateSerializer

    """def (self,request, *args, **kwargs):
        serializer = ImageCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.save()
        data = ImageModelSerializer(image).data
        return Response(data, status = status.HTTP_201_CREATED)"""