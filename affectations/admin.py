from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_utils import export_as_csv_action
from evaluations.models import EvaluationTuteurEcole, EvaluationTuteurEntreprise
from suivis.models import Livrable

from .models import Affectation
from .services import build_conventions_archive


class LivrableInline(admin.TabularInline):
    model = Livrable
    extra = 0
    fields = ("type", "due_date", "status", "score")
    readonly_fields = ("created_at", "updated_at")
    show_change_link = True


class EvaluationEntrepriseInline(admin.StackedInline):
    model = EvaluationTuteurEntreprise
    extra = 0
    max_num = 1
    can_delete = False
    fields = ("score", "evaluation_date", "evaluator", "feedback")


class EvaluationEcoleInline(admin.StackedInline):
    model = EvaluationTuteurEcole
    extra = 0
    max_num = 1
    can_delete = False
    fields = ("score", "evaluation_date", "evaluator", "feedback")


@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ("student", "entreprise", "start_date", "end_date", "status")
    list_filter = ("status", "entreprise", "start_date")
    search_fields = ("student__username", "entreprise__name")
    inlines = (LivrableInline, EvaluationEntrepriseInline, EvaluationEcoleInline)
    actions = ("exporter_en_csv", "generer_conventions_pdf")

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=(
                "id",
                "student",
                "entreprise",
                "start_date",
                "end_date",
                "status",
            ),
        )

    @admin.action(description=_("Générer les conventions (PDF)"))
    def generer_conventions_pdf(self, request, queryset):
        return build_conventions_archive(queryset)

