from django.contrib.auth.models import User
from rest_framework import serializers

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
        fields = ("pk", "name", "hub")


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля"""

    user = UserSerializer(label="Пользователь")
    car_loan_center = CarLoanCenterSerializer(label="ЦАК")

    class Meta:
        model = UserProfile
        fields = ("user", "car_loan_center")


class NotesBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для записок"""

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
    """Сериализатор для создания записок"""

    def create(self, validated_data):
        """Создаем записку"""
        request = self.context.get("request")
        user_profile = request.user.user_profile
        validated_data["owner"] = user_profile.pk
        validated_data["car_loan_center"] = user_profile.car_loan_center.pk
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Обновляем записку"""
        validated_data.pop("car_loan_center", None)
        return super().update(instance, validated_data)


class PermissionSerializer(serializers.Serializer):
    """Сериализатор для проверки прав пользователя"""

    can_filter_by_car_loan_center = serializers.SerializerMethodField(
        label="Разрешено фильтровать по ЦАК"
    )

    @staticmethod
    def get_can_filter_by_car_loan_center(user_profile, *args, **kwargs) -> bool:
        """Проверяем, есть ли у пользователя права на фильтрацию по ЦАК"""
        user = user_profile.user
        user_groups = user.groups.all().values_list("name", flat=True)
        return user_profile.HUB_LEADER_PERMISSION_NAME in user_groups

    class Meta:
        model = UserProfile
        fields = ("can_filter_by_car_loan_center",)
