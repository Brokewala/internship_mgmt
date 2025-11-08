from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_utils import export_as_csv_action

from .models import Alerte, AuditLog, Departement, Programme, Promotion


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "created_at")
    search_fields = ("code", "name")
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self, request, queryset, field_names=("id", "code", "name", "created_at")
        )


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "departement")
    search_fields = ("code", "title", "departement__name")
    list_filter = ("departement",)
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=("id", "code", "title", "departement"),
        )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("label", "programme", "year", "start_date", "end_date")
    list_filter = ("programme", "year")
    search_fields = ("label", "programme__title")
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=("id", "label", "programme", "year", "start_date", "end_date"),
        )


@admin.register(Alerte)
class AlerteAdmin(admin.ModelAdmin):
    list_display = ("titre", "niveau", "affectation", "resolue", "created_at")
    list_filter = ("niveau", "resolue", "created_at")
    search_fields = ("titre", "message", "affectation__student__username")
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=("id", "titre", "niveau", "affectation", "resolue", "created_at"),
        )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "actor", "occurred_at")
    list_filter = ("occurred_at",)
    search_fields = ("action", "actor__username")
    readonly_fields = ("metadata",)

