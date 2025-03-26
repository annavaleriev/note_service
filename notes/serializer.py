from django.contrib.auth.models import User
from rest_framework import serializers

from notes.models import Hub, CarLoanCenter, UserProfile, Notes


class HubSerializer(serializers.ModelSerializer):
    """Сериализатор для хаба"""

    class Meta:
        model = Hub
        fields = "__all__"

class CarLoanCenterSerializer(serializers.ModelSerializer):
    """Сериализатор для центра автокредитования"""

    class Meta:
        model = CarLoanCenter
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля"""

    user = serializers.StringRelatedField()
    car_loan_center = CarLoanCenterSerializer()

    class Meta:
        model = UserProfile
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class NotesSerializer(serializers.ModelSerializer):
    """Сериализатор для записок"""

    class Meta:
        model = Notes
        fields = ['owner', 'car_loan_center', 'created_at', 'subject', 'appoval_date', 'status']
