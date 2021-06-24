"""admin permissions"""

#Django REST Framework
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """ Handle of ensure that the request user is admin """
    def has_permission(self, request, view):
        return request.user.is_staff
