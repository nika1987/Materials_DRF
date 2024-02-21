from rest_framework.permissions import BasePermission


# Первый вариант
# ----------------------------------------------------------------
class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_moderator = request.user.groups.filter(name='moderator').exists()

        return obj.user == request.user or is_moderator


# Второй вариант (проверен)
# ----------------------------------------------------------------

class CustomPermission(BasePermission):
    '''Модератор имеет право смотреть и редактировать контент'''
    def has_permission(self, request, view):
        if not request.user.is_superuser and not request.user.is_staff:
            return True
        elif request.user.is_superuser:
            return True
        elif request.method in ['GET', 'PUT', 'PATCH'] and request.user.is_staff:
            return True
        else:
            return False
