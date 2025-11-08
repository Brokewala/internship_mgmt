from django.contrib import admin

from .models import Suivi


@admin.register(Suivi)
class SuiviAdmin(admin.ModelAdmin):
    list_display = ("affectation", "meeting_date", "created_at")
    list_filter = ("meeting_date",)
    search_fields = ("affectation__student__username", "affectation__entreprise__name")

