from datetime import date

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from notes.filters import CarLoanCenterFilter, NotesFilter, UserProfileFilter
from notes.models import CarLoanCenter, Hub, Notes, UserProfile
from notes.permissions import (CanCreate, CanUserDeleteNotes,
                               HasUserProfilePermission, CanChange, CanApproved, CanClone)
from notes.serializer import (CarLoanCenterSerializer, HubSerializer,
                              NotesCreateSerializer, NotesSerializer,
                              PermissionSerializer, UserProfileSerializer)


def check_user_access(user_profile, note):
    """Проверяет доступ пользователя к записке"""

    if (
        note.owner != user_profile
        and not note.observers.filter(id=user_profile.id).exists()
    ):
        raise PermissionDenied("У вас нет доступа для записки в этом ЦАК")
    return True


class UserProfileViewSet(mixins.ListModelMixin, GenericViewSet):
    """ViewSet для профиля пользователя"""

    queryset = UserProfile.objects.all().order_by("car_loan_center")
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, HasUserProfilePermission]
    filterset_class = UserProfileFilter
    filter_backends = [DjangoFilterBackend]

    @action(serializer_class=PermissionSerializer, detail=False)
    def permissions(self, request):
        """Возвращает права пользователя"""
        user_profile = self.request.user.userprofile
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)


class HubViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для хаба"""

    queryset = Hub.objects.all().order_by("name")
    serializer_class = HubSerializer
    permission_classes = [IsAuthenticated, HasUserProfilePermission]
    filter_backends = [DjangoFilterBackend]


class CarLoanCenterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для центра автокредитования"""

    queryset = CarLoanCenter.objects.all().order_by("name")
    serializer_class = CarLoanCenterSerializer
    permission_classes = [IsAuthenticated, HasUserProfilePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarLoanCenterFilter


class NotesViewSet(viewsets.ModelViewSet):
    """ViewSet для записок"""

    queryset = Notes.objects.all().order_by("subject")
    serializer_class = NotesSerializer
    permission_classes = [
        IsAuthenticated,
        HasUserProfilePermission,
        CanUserDeleteNotes,
        CanCreate,
        CanChange
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NotesFilter

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от действия"""

        if self.action in ("create", "update", "partial_update"):
            return NotesCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """Возвращает список записок, где пользователь является владельцем или наблюдателем"""
        queryset = super().get_queryset()
        user_profile: UserProfile = self.request.user.userprofile

        if user_profile.in_go_group or user_profile.in_oskp_group:
            return queryset

        if user_profile.in_hub_leader_group:
            return queryset.filter(car_loan_center__hub=user_profile.car_loan_center.hub)

        return queryset.filter(
            Q(car_loan_center=user_profile.car_loan_center)
            & (Q(owner=user_profile) | Q(observers=user_profile))
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, HasUserProfilePermission, CanApproved])
    def approved(self, request, pk=None):
        """Согласование записки"""
        note = self.get_object()
        note.apr_date = date.today()
        note.save()
        return Response(
            {
                "approve": "Согласование прошло успешно"
            }
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, HasUserProfilePermission, CanClone])
    def clone(self, request, pk=None):
        """Клонирование записки, Копировать СЗ как нулевую
 (Копирование с обрывом связи с родительской СЗ)"""
        note = self.get_object()
        note.pyrus_url = None
        note.pk = None
        note.save()
        serializer = self.get_serializer(note)
        return Response(serializer.data)
