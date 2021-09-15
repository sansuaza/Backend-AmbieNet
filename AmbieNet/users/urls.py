"""Users URLs."""

#Django
from django.urls import include, path

# Django REST Framework
"""Genera todos los paths del viewset de manera automática"""
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views
from .views import admins as admin_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')
router.register(r'staffs', admin_views.AdminViewSet, basename='staffs')

urlpatterns = [
    path('', include(router.urls))
]
