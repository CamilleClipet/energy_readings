from django.contrib import admin
from django.db.models import Q, Value, QuerySet
from django.db.models.functions import Replace
from django.http import HttpRequest
from typing import Tuple
from .models import File, Reading

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'import_time')
    search_fields = ('file_name',)
    ordering = ('-import_time',)

@admin.register(Reading)
class ReadingsAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'mpan_core', 'validation_status', 'meter_id', 'reading_type', 'meter_register_id','reading_datetime', 'register_reading', 'md_reset_datetime', 'nb_md_resets', 'meter_reading_flag', 'reading_method', 'meter_reading_reason_code', 'meter_reading_status')
    search_fields = ('mpan_core',)
    ordering = ('-reading_datetime',)

    def get_search_results(self, request: HttpRequest, queryset: QuerySet, search_term: str) -> Tuple[QuerySet, bool]:
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        
        if search_term:
            # Allow the search to succeed if the user forgets the space in the meter_id
            queryset |= self.model.objects.annotate(
                meter_id_no_spaces=Replace('meter_id', Value(' '), Value(''))
            ).filter(meter_id_no_spaces__iexact=search_term.replace(" ", ""))
        
        return queryset, may_have_duplicates
