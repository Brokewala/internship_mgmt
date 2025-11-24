from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from core.admin_mixins import AdminPageDescriptionMixin, AuditLogAdminMixin
from core.admin_utils import export_as_csv_action
from evaluations.models import EvaluationTuteurEcole, EvaluationTuteurEntreprise
from suivis.models import Livrable

from .models import Affectation
from .services import build_convention_pdf_response, build_conventions_archive
from core.services.emails import send_assignment_reminder_email


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
class AffectationAdmin(AdminPageDescriptionMixin, AuditLogAdminMixin, admin.ModelAdmin):
    page_description = (
        "Affectations d'étudiants en entreprise avec dates, statut, livrables et évaluations."
    )
    list_display = ("student", "entreprise", "start_date", "end_date", "status")
    list_filter = ("status", "entreprise", "start_date")
    search_fields = ("student__username", "entreprise__name")
    inlines = (LivrableInline, EvaluationEntrepriseInline, EvaluationEcoleInline)
    actions = ("exporter_en_csv", "generer_conventions_pdf")
    change_form_template = "admin/affectations/affectation/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/generer-convention/",
                self.admin_site.admin_view(self.generer_convention_view),
                name="affectations_affectation_generate_convention",
            ),
            path(
                "<path:object_id>/envoyer-rappel/",
                self.admin_site.admin_view(self.envoyer_rappel_view),
                name="affectations_affectation_send_reminder",
            ),
        ]
        return custom_urls + urls

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

    def generer_convention_view(self, request, object_id):
        affectation = self.get_object(request, object_id)
        if not affectation:
            messages.error(request, _("Affectation introuvable."))
            return HttpResponseRedirect(reverse("admin:affectations_affectation_changelist"))
        return build_convention_pdf_response(affectation)

    def envoyer_rappel_view(self, request, object_id):
        affectation = self.get_object(request, object_id)
        if not affectation:
            messages.error(request, _("Affectation introuvable."))
            return HttpResponseRedirect(reverse("admin:affectations_affectation_changelist"))

        sent = send_assignment_reminder_email(affectation)
        if sent:
            messages.success(
                request,
                _("Un email de rappel a été envoyé à l'étudiant."),
            )
        else:
            messages.warning(
                request,
                _("Impossible d'envoyer le rappel : aucune adresse email renseignée."),
            )
        return HttpResponseRedirect(
            reverse("admin:affectations_affectation_change", args=[object_id])
        )

