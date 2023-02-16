from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class CheckAccessReview(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            raise PermissionDenied('Анонимному пользователю '
                                   'запрещено создавать запись')

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        ):
            raise PermissionDenied('Запрещено редактировать '
                                   'чужие записи')
