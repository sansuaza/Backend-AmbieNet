"""Post URLs."""

#Django
from django.urls import path

#Views
from AmbieNet.posts.views import PostCreateApiView

urlpatterns=[
    path('posts/create/', PostCreateApiView.as_view(), name='create')
]