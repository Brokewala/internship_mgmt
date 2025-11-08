from django.contrib import admin

from .models import OffreStage


@admin.register(OffreStage)
class OffreStageAdmin(admin.ModelAdmin):
    list_display = ("title", "entreprise", "location", "start_date", "status")
    search_fields = ("title", "entreprise__name")
    list_filter = ("status", "location", "entreprise")

