from django.contrib import admin

from core.admin_mixins import AdminPageDescriptionMixin

from .models import ReportSnapshot


@admin.register(ReportSnapshot)
class ReportSnapshotAdmin(AdminPageDescriptionMixin, admin.ModelAdmin):
    page_description = (
        "Instantanés de reporting générés automatiquement avec totaux consolidés."
    )
    list_display = ("generated_at", "total_students", "total_offers", "total_assignments")
    readonly_fields = ("generated_at",)

