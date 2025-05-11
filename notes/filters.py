import django_filters
from django.db.models import Q

from notes.models import CarLoanCenter, Notes, UserProfile


class NotesFilter(django_filters.FilterSet):
    """
    Фильтр по запискам
    pyrus_url - фильтр по ссылке на Pyrus
    status - фильтр по статусу записки
    subject - фильтр по теме записки
    name - фильтр по имени и фамилии автора записки
    """

    pyrus_url = django_filters.CharFilter(
        field_name="pyrus_url", label="Cсылка на Pyrus", lookup_expr="icontains"
    )
    status = django_filters.MultipleChoiceFilter(
        choices=Notes.StatusNotes.choices, label="Статус записки"
    )
    subject = django_filters.CharFilter(
        field_name="subject", lookup_expr="icontains", label="Тема записки"
    )
    name = django_filters.CharFilter(
        method="get_filtered_by_name",
        label="Автор записки. Разрешен частичный поиск по Фамилии и Имени",
    )

    @staticmethod
    def get_filtered_by_name(queryset, _, search_text, *args, **kwargs):
        """Фильтр по имени и фамилии автора записки"""
        return queryset.select_related("owner", "owner__user").filter(
            Q(owner__user__last_name__icontains=search_text)
            | Q(owner__user__first_name__icontains=search_text)
        )

    class Meta:
        model = Notes
        fields = ("pyrus_url", "status", "subject", "name", "car_loan_center")


class UserProfileFilter(django_filters.FilterSet):
    """Фильтр по пользователям"""

    name = django_filters.CharFilter(
        method="get_filtered_by_name",
        label="Автор записки. Разрешен частичный поиск по Фамилии и Имени",
    )

    @staticmethod
    def get_filtered_by_name(queryset, _, search_text, *args, **kwargs):
        """Фильтр по имени и фамилии пользователя"""
        return queryset.select_related("user").filter(
            Q(user__last_name__icontains=search_text)
            | Q(user__first_name__icontains=search_text)
        )

    class Meta:
        model = UserProfile
        fields = ("name",)


class CarLoanCenterFilter(django_filters.FilterSet):
    """Фильтр по центру автокредитования"""

    name = django_filters.CharFilter(
        lookup_expr="icontains", required=False, label="Центр автокредитования"
    )

    class Meta:
        model = CarLoanCenter
        fields = ("name",)
