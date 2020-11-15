
#Django REST Framework
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
   """Allow the admin sometimes actions."""

   def has_admin_role(self, request, view, obj):
       return request.user.is_staff == True
