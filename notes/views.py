from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, viewsets
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
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для хаба"""

    queryset = Hub.objects.all().order_by("name")
    serializer_class = HubSerializer
    permission_classes = [IsAuthenticated]


# class CarLoanCenterViewSet(viewsets.ReadOnlyModelViewSet):
#     """ViewSet для центра автокредитования"""
#
#     queryset = CarLoanCenter.objects.all().order_by("name")
#     serializer_class = CarLoanCenterSerializer
#     permission_classes = [IsAuthenticated]
#
#     def create (self, request, *args, **kwargs):
#         """Создание новой записи"""
#         serializer = self.get_serializer(data=request.data) # Создаем сериализатор
#         serializer.is_valid(raise_exception=True) # Проверяем валидность данных
#         self.perform_create(serializer) # Сохраняем данные
#         headers = self.get_success_headers(serializer.data) # Получаем заголовки ответа
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) # Возвращаем ответ с данными и статусом 201 Created


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
