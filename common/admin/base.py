from django.contrib import admin


class SelectPrefetchRelatedModelAdmin(admin.ModelAdmin):
    """Миксин для админки, который позволяет использовать select_related в queryset"""

    select_related_fields = []
    prefetch_related_fields = []

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        return queryset
