from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from notes.filters import NotesFilter
from notes.models import CarLoanCenter, Hub, Notes
from notes.serializer import (
    CarLoanCenterSerializer,
    HubSerializer,
    NotesCreateSerializer,
    NotesSerializer,
)


class HubViewSet(
    viewsets.ReadOnlyModelViewSet
):
    """ViewSet для хаба"""

    queryset = Hub.objects.all().order_by("name")
    serializer_class = HubSerializer
    permission_classes = [IsAuthenticated]


class CarLoanCenterViewSet(
    viewsets.ReadOnlyModelViewSet
):
    """ViewSet для центра автокредитования"""

    queryset = CarLoanCenter.objects.all().order_by("name")
    serializer_class = CarLoanCenterSerializer
    permission_classes = [IsAuthenticated]


class NotesViewSet(viewsets.ModelViewSet):
    """ViewSet для записок"""

    queryset = Notes.objects.all().order_by("subject")
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NotesFilter

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return NotesCreateSerializer
        return super().get_serializer_class()
