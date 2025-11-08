from django.contrib import admin

from .models import Affectation


@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ("student", "entreprise", "start_date", "end_date", "status")
    list_filter = ("status", "entreprise")
    search_fields = ("student__username", "entreprise__name")

