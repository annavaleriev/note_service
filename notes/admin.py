from django.contrib import admin

from notes.models import UserProfile, CarLoanCenter


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ("user", "car_loan_center")
    list_display = ("user", "car_loan_center")


@admin.register(CarLoanCenter)
class CarLoanCenterAdmin(admin.ModelAdmin):
    fields = ("name", "hub")
    list_display = ("name", "hub")
