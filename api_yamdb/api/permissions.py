from rest_framework import permissions


class SelfEditUserOnlyPermission(permissions.BasePermission):
    """Доступ к users/me только юзерам."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.id == request.user)


class IsAdminOnlyPermission(permissions.BasePermission):
    """Доступ только aдмину."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        return False
