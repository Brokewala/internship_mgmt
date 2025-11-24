from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_mixins import AdminPageDescriptionMixin
from core.admin_utils import export_as_csv_action

from .models import ContactEntreprise, Entreprise


class ContactEntrepriseInline(admin.TabularInline):
    model = ContactEntreprise
    extra = 1
    fields = ("first_name", "last_name", "email", "phone", "role")
    show_change_link = True


@admin.register(Entreprise)
class EntrepriseAdmin(AdminPageDescriptionMixin, admin.ModelAdmin):
    page_description = (
        "Fiches entreprises avec coordonnées principales et contacts associés."
    )
    list_display = ("name", "website", "contact_email", "created_at")
    search_fields = ("name", "contact_email", "contacts__last_name")
    list_filter = ("created_at",)
    inlines = (ContactEntrepriseInline,)
    actions = ("exporter_en_csv",)

    @admin.action(description=_("Exporter la sélection en CSV"))
    def exporter_en_csv(self, request, queryset):
        return export_as_csv_action(
            self,
            request,
            queryset,
            field_names=("id", "name", "contact_email", "website", "created_at"),
        )

