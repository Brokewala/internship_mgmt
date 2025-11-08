from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Evaluation


class EvaluationListView(LoginRequiredMixin, ListView):
    model = Evaluation
    template_name = "evaluations/evaluation_list.html"
    context_object_name = "evaluations"

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(affectation__student=self.request.user)
        return qs

