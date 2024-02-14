from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return True
        else:
            return False
