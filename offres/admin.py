from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from candidatures.models import Candidature
from core.admin_mixins import AdminPageDescriptionMixin
from core.admin_utils import export_as_csv_action

from .models import OffreStage


class CandidatureInline(admin.TabularInline):
    model = Candidature
    extra = 0
    fields = ("student", "status", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(OffreStage)
class OffreStageAdmin(AdminPageDescriptionMixin, admin.ModelAdmin):
    page_description = (
        "Offres de stage associées à une entreprise et une campagne avec localisation, dates et statut."
    )
    list_display = (
        "title",
        "entreprise",
        "campagne",
        "location",
        "start_date",
        "status",
    )
    search_fields = ("title", "entreprise__name", "campagne__title")
    list_filter = ("status", "location", "entreprise", "campagne")
    inlines = (CandidatureInline,)
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=(
                "id",
                "title",
                "entreprise",
                "campagne",
                "location",
                "start_date",
                "end_date",
                "status",
            ),
        )

