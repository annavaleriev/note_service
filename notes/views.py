from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from notes.models import CarLoanCenter, Hub, Notes, UserProfile
from notes.serializer import (CarLoanCenterSerializer, HubSerializer,
                              NotesCreateSerializer, NotesSerializer,
                              UserProfileSerializer)


class UserProfileViesSet(viewsets.ModelViewSet):
    """ViewSet для профиля пользователя"""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class HubViewSet(viewsets.ModelViewSet):
    """ViewSet для хаба"""

    queryset = Hub.objects.all()
    serializer_class = HubSerializer
    permission_classes = [IsAuthenticated]


class CarLoanCenterViewSet(viewsets.ModelViewSet):
    """ViewSet для центра автокредитования"""

    queryset = CarLoanCenter.objects.all()
    serializer_class = CarLoanCenterSerializer
    permission_classes = [IsAuthenticated]


class NotesViewSet(viewsets.ModelViewSet):
    """ViewSet для записок"""

    queryset = Notes.objects.all().order_by("subject")
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return NotesCreateSerializer
        return super().get_serializer_class()
