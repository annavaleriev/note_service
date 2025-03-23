from django.contrib import admin

from notes.models import UserProfile, CarLoanCenter, Hub, Notes


# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ("user", "car_loan_center")
    list_display = ("user", "car_loan_center")


@admin.register(CarLoanCenter)
class CarLoanCenterAdmin(admin.ModelAdmin):
    fields = ("name", "hub")
    list_display = ("name", "hub")

@admin.register(Hub)
class HubAdmin(admin.ModelAdmin):
    fields = ("name", )
    list_display = ("name", )


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    fields = ("parus_url", "car_loan_center", "created_at", "update_at", "appoval_date", "subject", "owner",
              "observers", "status")
    list_display = ("parus_url", "car_loan_center", "created_at", "update_at", "appoval_date", "subject", "owner",
                    "get_observers", "status")
    list_filter = ("parus_url", "car_loan_center", "created_at", "update_at", "appoval_date", "subject", "owner",
                     "status")
    search_fields = ("car_loan_center", "owner", "created_at", "subject", "status", "update_at", "appoval_date",
                     "observers", "parus_url")

    def get_observers(self, obj):
        return ",".join([user.username for user in obj.observers.all()])
    get_observers.short_description = "Observers"

