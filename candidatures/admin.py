from django.contrib import admin

from .models import Candidature


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ("student", "offer", "status", "created_at")
    list_filter = ("status", "offer__entreprise")
    search_fields = ("student__username", "offer__title")

