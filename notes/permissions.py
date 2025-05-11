from rest_framework.permissions import BasePermission


class HasUserProfilePermission(BasePermission):
    """Проверяет, есть ли у пользователя профиль"""

    def has_object_permission(self, request, view, obj):
        """Проверяет, есть ли у пользователя профиль"""
        has_permission = super().has_object_permission(request, view, obj)
        user_profile = request.user.userprofile
        return has_permission and user_profile

    def has_permission(self, request, view):
        """Проверяет, есть ли у пользователя профиль"""
        has_permission = super().has_permission(request, view)
        user_profile = request.user.userprofile
        return has_permission and user_profile
