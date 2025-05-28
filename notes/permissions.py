from rest_framework.permissions import SAFE_METHODS, BasePermission

from notes.models import UserProfile


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


class CanUserDeleteNotes(BasePermission):
    """Проверяет, может ли пользователь удалить записку"""

    def has_object_permission(self, request, view, obj):
        """Проверяет, может ли пользователь удалить записку"""
        if request.method == "DELETE":
            user_profile: UserProfile = request.user.userprofile
            has_hub_object = (
                obj.car_loan_center.hub.pk == user_profile.car_loan_center.hub.pk
            )
            is_owner = user_profile == obj.owner

            return (
                user_profile.in_oskp_group
                or (user_profile.in_hub_leader_group and has_hub_object)
                or is_owner
            )

        return super().has_object_permission(request, view, obj)


class CanCreate(BasePermission):
    """Проверяет, может ли пользователь создавать записки"""

    def has_permission(self, request, view):
        """Проверяет, может ли пользователь создавать записки"""
        user_profile = request.user.userprofile
        if request.method == "POST":
            in_osk_or_go_group = user_profile.in_go_group or user_profile.in_oskp_group
            return (
                user_profile.in_hub_leader_group
                and request.data.get("car_loan_center")
                != user_profile.car_loan_center.pk
            ) or not in_osk_or_go_group

        return super().has_permission(request, view)


class CanChange(BasePermission):
    """Проверяет, может ли пользователь изменять записки"""

    def has_permission(self, request, view):
        """Проверяет, может ли пользователь изменять записки"""
        user_profile = request.user.userprofile
        if request.method in ("PUT", "PATCH"):
            if user_profile.in_go_group:
                return False

        return super().has_permission(request, view)

    # def has_object_permission(self, request, view, obj):
    #     user_profile = request.user.userprofile
    #     if (user_profile.in_go_group or user_profile.in_oskp_group) and request.method == "POST":
    #         return False
    #
    #     return True


# class GOPermission(BasePermission):
#     """
#     Проверяет, есть ли у пользователя группа GO
#     Видят все СЗ
#     Только чтение (GET, HEAD, OPTIONS)
#     """
#
#     def has_permission(self, request, view):
#         user_profile = request.user.userprofile
#         if user_profile.in_go_group:
#             return request.method in SAFE_METHODS
#         return True
#
#     def has_object_permission(self, request, view, obj):
#         user_profile = request.user.userprofile
#         if user_profile.in_go_group:
#             return request.method in SAFE_METHODS
#         return True


# class OSKPPermission(BasePermission):
#     """
#     Проверяет, есть ли у пользователя группа ОСКП
#     Видят все СЗ
#     Могут редактировать, удалять, согласовывать, копировать
#     Не могут создавать
#     """
#
#     def has_permission(self, request, view):
#         user_profile: UserProfile = request.user.userprofile
#         if user_profile and user_profile.in_oskp_group and request.method == "POST":
#             return False
#         return True
#
#     def has_object_permission(self, request, view, obj):
#         user_profile = request.user.userprofile
#         return user_profile and user_profile.in_oskp_group


# class HubLeaderPermission(BasePermission):
#     """
#     Проверяет, есть ли у пользователя группа ХАБ Лидер
#     Видят  СЗ своего Хаба
#     Могут редактировать, удалять, копировать видимые СЗ
#     Не могут согласовывать и администрировать
#     Могут создавать СЗ только под Цаком своего Хаба
#     """
#
#     def has_permission(self, request, view):
#         user_profile: UserProfile = request.user.userprofile
#         if user_profile and user_profile.in_hub_leader_group:
#             if request.method == "POST":
#                 # Проверяем, что ЦАК в запросе совпадает с ЦАК пользователя
#                 if request.data.get("car_loan_center") != user_profile.car_loan_center.pk:
#                     return False
#             return True
#
#     def has_object_permission(self, request, view, obj):
#         user_profile = request.user.userprofile
#         if user_profile and user_profile.in_hub_leader_group:
#             if request.method in SAFE_METHODS or request.method in ("PUT", "PATCH", "DELETE"):
#                 if obj.hub.pk == user_profile.car_loan_center.hub.pk:
#                     return True
#
#         if view.action == ("approved", "administration") :
#             return False
#
#         return False
