from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from notes.models import CarLoanCenter, Hub, Notes, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ("first_name", "last_name")


class HubSerializer(serializers.ModelSerializer):
    """Сериализатор для хаба"""

    class Meta:
        model = Hub
        fields = ("name",)


class CarLoanCenterSerializer(serializers.ModelSerializer):
    """Сериализатор для центра автокредитования"""

    hub = HubSerializer(label="ХАБ")

    class Meta:
        model = CarLoanCenter
        fields = ("name", "hub")


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля"""

    user = UserSerializer(label="Пользователь")
    car_loan_center = CarLoanCenterSerializer(label="ЦАК")

    class Meta:
        model = UserProfile
        fields = ("user", "car_loan_center")


class NotesBaseSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(label="Владелец", read_only=True)

    class Meta:
        model = Notes
        fields = (
            "id",
            "pyrus_url",
            "car_loan_center",
            "appoval_date",
            "subject",
            "observers",
            "owner",
        )


class NotesSerializer(NotesBaseSerializer):
    """Сериализатор для записок"""

    car_loan_center = CarLoanCenterSerializer(label="ЦАК")

    class Meta(NotesBaseSerializer.Meta):
        fields = NotesBaseSerializer.Meta.fields + ("created_at", "update_at", "status")


class NotesCreateSerializer(NotesBaseSerializer):
    def create(self, validated_data):
        request = self.context.get("request")
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if not user_profile:
            raise ValidationError("У вас нет доступа для создания СЗ")
        instance = super().create(validated_data)
        instance.owner = user_profile
        instance.save()
        return instance
