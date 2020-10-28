"""Post URLs."""

#Django
from django.urls import path

#Views
from AmbieNet.posts.views import PostCreateApiView
from AmbieNet.posts.views import ImageCreateApiView

urlpatterns=[
    path('posts/create/', PostCreateApiView.as_view(), name='create'),
    path('posts/image/', ImageCreateApiView.as_view(), name='image')
]