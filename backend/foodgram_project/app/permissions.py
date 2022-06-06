from rest_framework import permissions


class OwnerOrAdminOrReadOnly(permissions.BasePermission):
    message = ('Только автор или администратор может вносить изменения!')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
