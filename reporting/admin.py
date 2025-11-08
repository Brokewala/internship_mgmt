from django.contrib import admin

from .models import ReportSnapshot


@admin.register(ReportSnapshot)
class ReportSnapshotAdmin(admin.ModelAdmin):
    list_display = ("generated_at", "total_students", "total_offers", "total_assignments")
    readonly_fields = ("generated_at",)

