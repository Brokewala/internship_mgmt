from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_utils import export_as_csv_action

from .models import Journal, Livrable, Suivi


@admin.register(Suivi)
class SuiviAdmin(admin.ModelAdmin):
    list_display = ("affectation", "meeting_date", "created_at")
    list_filter = ("meeting_date",)
    search_fields = ("affectation__student__username", "affectation__entreprise__name")


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("affectation", "entry_date", "created_at")
    list_filter = ("entry_date", "affectation__entreprise")
    search_fields = ("affectation__student__username", "content")
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=("id", "affectation", "entry_date", "created_at"),
        )


@admin.register(Livrable)
class LivrableAdmin(admin.ModelAdmin):
    list_display = (
        "affectation",
        "type",
        "title",
        "due_date",
        "status",
        "score",
    )
    list_filter = ("type", "status", "due_date")
    search_fields = ("title", "affectation__student__username", "affectation__entreprise__name")
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=(
                "id",
                "affectation",
                "type",
                "due_date",
                "submitted_at",
                "status",
                "score",
            ),
        )

