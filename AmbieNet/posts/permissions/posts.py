#Django REST Framework
from rest_framework.permissions import BasePermission

class IsPostOwner(BasePermission):
	"""Allow the post owner sometime actions."""
	
	def has_object_permission(self, request, view, obj):
		return request.user == obj.user
