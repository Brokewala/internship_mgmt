from django.contrib import admin

from .models import Entreprise


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "contact_email")
    search_fields = ("name", "contact_email")

