from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_mixins import AdminPageDescriptionMixin, AuditLogAdminMixin
from .models import Candidature


@admin.register(Candidature)
class CandidatureAdmin(AdminPageDescriptionMixin, AuditLogAdminMixin, admin.ModelAdmin):
    page_description = (
        "Candidatures des étudiants aux offres avec statut et actions de décision."
    )
    list_display = ("student", "offer", "status", "created_at")
    list_filter = ("status", "offer__entreprise")
    search_fields = ("student__username", "offer__title")
    actions = ("accepter_candidatures", "refuser_candidatures")

    @admin.action(description=_("Accepter les candidatures sélectionnées"))
    def accepter_candidatures(self, request, queryset):
        updated = 0
        for candidature in queryset:
            before = self._serialize_for_audit(candidature)
            candidature.status = Candidature.Status.ACCEPTED
            candidature.save(update_fields=["status"])
            updated += 1
            after = self._serialize_for_audit(candidature)
            self._log_audit_event(
                request,
                action=self._get_audit_action_label(candidature, change=True),
                obj=candidature,
                before=before,
                after=after,
            )
        self.message_user(
            request,
            _("%(count)s candidature(s) ont été acceptées.") % {"count": updated},
        )

    @admin.action(description=_("Refuser les candidatures sélectionnées"))
    def refuser_candidatures(self, request, queryset):
        updated = 0
        for candidature in queryset:
            before = self._serialize_for_audit(candidature)
            candidature.status = Candidature.Status.REJECTED
            candidature.save(update_fields=["status"])
            updated += 1
            after = self._serialize_for_audit(candidature)
            self._log_audit_event(
                request,
                action=self._get_audit_action_label(candidature, change=True),
                obj=candidature,
                before=before,
                after=after,
            )
        self.message_user(
            request,
            _("%(count)s candidature(s) ont été refusées.") % {"count": updated},
        )

