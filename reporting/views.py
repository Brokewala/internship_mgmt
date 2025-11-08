from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import ReportSnapshot


class ReportSnapshotListView(LoginRequiredMixin, ListView):
    model = ReportSnapshot
    template_name = "reporting/report_list.html"
    context_object_name = "reports"

