import django_filters
from django.db.models import Q

from notes.models import Notes


class NotesFilter(django_filters.FilterSet):
    """ Фильтр по запискам """

    # Фильтр по ссылке на Pyrus
    parus_url = django_filters.CharFilter(method="filter_parus_url", required=False, label="Cсылка на Pyrus")

    @staticmethod
    def filter_parus_url(queryset, name, value):
        if value and value.startswith("https://pyrus.sovcombank.ru/"):
            return queryset.filter(**{name + "__icontains": value})
        return queryset.none()

    # Фильтр по статусу
    status = django_filters.MultipleChoiceFilter(choices=Notes.StatusNotes.choices, required=False, label="Статус записки")

    # Фильтр по теме записки
    subject = django_filters.CharFilter(lookup_expr="icontains", required=False, label="Тема записки")

    # Фильтр по имени
    name = django_filters.CharFilter(method="get_filtered_by_name", required=False, label="Автор записки")

    @staticmethod
    def get_filtered_by_name(queryset, _, search_text):
        return queryset.filter(Q(owner__user__last_name__icontains=search_text))

    class Meta:
        model = Notes
        fields = ("status", "name")


# class NotesFilterByStatus(django_filters.FilterSet):
#     """ Фильтр для поиска записок по статусу """
#
#     status = django_filters.ChoiceFilter(choices=Notes.StatusNotes.choices)
#
#     class Meta:
#         model = Notes
#         fields = ("status",)


class CarLoanCenterFilter(django_filters.FilterSet):
    """ Фильтр по центру автокредитования """

    # Фильтр по названию центра автокредитования
    name = django_filters.CharFilter(lookup_expr="icontains", required=False, label="Центр автокредитования")

    class Meta:
        model = Notes
        fields = ("name",)
