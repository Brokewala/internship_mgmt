from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_mixins import AdminPageDescriptionMixin
from core.admin_utils import export_as_csv_action

from .models import EvaluationTuteurEcole, EvaluationTuteurEntreprise, NoteFinale


class BaseEvaluationAdmin(AdminPageDescriptionMixin, admin.ModelAdmin):
    page_description = (
        "Évaluations des tuteurs pour une affectation donnée avec score, date et évaluateur."
    )
    list_display = ("affectation", "evaluator", "score", "evaluation_date")
    list_filter = ("evaluation_date",)
    search_fields = ("affectation__student__username", "affectation__entreprise__name")
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=("id", "affectation", "score", "evaluation_date", "evaluator"),
        )


@admin.register(EvaluationTuteurEntreprise)
class EvaluationTuteurEntrepriseAdmin(BaseEvaluationAdmin):
    page_description = (
        "Évaluations réalisées par le tuteur en entreprise sur la mission de l'étudiant."
    )
    list_filter = BaseEvaluationAdmin.list_filter + ("score",)


@admin.register(EvaluationTuteurEcole)
class EvaluationTuteurEcoleAdmin(BaseEvaluationAdmin):
    page_description = (
        "Évaluations réalisées par le tuteur école pour suivre la progression académique."
    )
    list_filter = BaseEvaluationAdmin.list_filter + ("score",)


@admin.register(NoteFinale)
class NoteFinaleAdmin(AdminPageDescriptionMixin, admin.ModelAdmin):
    page_description = (
        "Notes finales calculées pour chaque affectation avec coefficients appliqués."
    )
    list_display = (
        "affectation",
        "valeur",
        "coefficient_entreprise",
        "coefficient_ecole",
        "coefficient_livrables",
        "updated_at",
    )
    search_fields = ("affectation__student__username", "affectation__entreprise__name")
    list_filter = ("valeur",)
    readonly_fields = ("valeur",)

