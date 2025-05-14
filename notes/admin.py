from django.contrib import admin
from django.utils.html import format_html

from common.admin.base import SelectPrefetchRelatedModelAdmin
from notes.models import CarLoanCenter, Hub, Notes, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(SelectPrefetchRelatedModelAdmin):
    """Админка для профиля пользователя"""





    select_related_fields = ("user", "car_loan_center")
    fields = ("user", "car_loan_center")
    list_display = ("user", "car_loan_center")
    search_fields = ("user__last_name", "user__first_name")
    list_filter = ("car_loan_center",)


@admin.register(CarLoanCenter)
class CarLoanCenterAdmin(SelectPrefetchRelatedModelAdmin):
    """Админка для центра автокредитования"""

    select_related_fields = ("hub",)
    fields = ("name", "hub")
    list_display = ("name", "hub")
    search_fields = ("name",)
    list_filter = ("hub", "name")


@admin.register(Hub)
class HubAdmin(admin.ModelAdmin):
    """Админка для ХАБ"""

    fields = ("name",)
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Notes)
class NotesAdmin(SelectPrefetchRelatedModelAdmin):
    """Админка для записок"""

    select_related_fields = ("car_loan_center", "owner")
    prefetch_related_fields = ("observers",)

    fieldsets = (
        (
            "Общая информация",
            {
                "fields": (
                    "subject",
                    "pyrus_url",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Остальное",
            {
                "fields": (
                    "car_loan_center",
                    "status",
                    "owner",
                    "observers",
                    "appoval_date",
                    "created_at",
                    "update_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    list_display = (
        "subject",
        "pyrus_url",
        "car_loan_center",
        "appoval_date",
        "owner",
        "get_observers",
        "status",
    )
    list_filter = (
        "car_loan_center",
        "created_at",
        "update_at",
        "appoval_date",
        "status",
    )
    search_fields = (
        "owner__user__last_name",
        "owner__user__first_name",
        "subject",
        "pyrus_url",
    )
    readonly_fields = (
        "created_at",
        "update_at",
        "get_observers",
    )
    filter_horizontal = ("observers",)
    autocomplete_fields = ("car_loan_center", "owner", "observers")

    def get_observers(self, obj):
        """Получаем наблюдателей"""
        return format_html(
            "<br>".join(
                [
                    f"{user_profile.user.last_name} {user_profile.user.first_name}"
                    for user_profile in obj.observers.all()
                ]
            )
        )

    get_observers.short_description = "Наблюдатели"
