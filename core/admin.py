from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_mixins import AdminPageDescriptionMixin, AuditLogAdminMixin
from core.admin_utils import export_as_csv_action

from .models import Departement, Programme, Promotion


@admin.register(Departement)
class DepartementAdmin(AdminPageDescriptionMixin, AuditLogAdminMixin, admin.ModelAdmin):
    page_description = (
        "Départements académiques utilisés pour structurer les programmes et promotions."
    )
    list_display = ("code", "name", "created_at")
    search_fields = ("code", "name")
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self, request, queryset, field_names=("id", "code", "name", "created_at")
        )


@admin.register(Programme)
class ProgrammeAdmin(AdminPageDescriptionMixin, AuditLogAdminMixin, admin.ModelAdmin):
    page_description = (
        "Programmes rattachés à un département avec code, intitulé et rattachement."
    )
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
class PromotionAdmin(AdminPageDescriptionMixin, AuditLogAdminMixin, admin.ModelAdmin):
    page_description = (
        "Promotions par programme avec année et dates clés pour organiser les campagnes."
    )
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


