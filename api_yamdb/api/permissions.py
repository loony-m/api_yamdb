from rest_framework import permissions


class CheckAccessReview(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
                )


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


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для пользователей c правами администратора или на чтение."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.method in permissions.SAFE_METHODS
        )
