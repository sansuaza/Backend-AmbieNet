
"""Posts URLs."""

#Django
from django.urls import include, path

# Django REST Framework
"""Genera todos los paths del viewset de manera automática"""
from rest_framework.routers import DefaultRouter

# Views
from .views import posts as post_views
from .views import images as image_views



router = DefaultRouter()
router.register(r'posts', post_views.PostViewSet, basename='posts')
router.register(r'images', image_views.ImageViewSet, basename='images')

urlpatterns = [
    path('', include(router.urls))
]