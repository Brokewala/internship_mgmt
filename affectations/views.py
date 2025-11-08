from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Affectation


class AffectationListView(LoginRequiredMixin, ListView):
    model = Affectation
    template_name = "affectations/affectation_list.html"
    context_object_name = "affectations"

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(student=self.request.user)
        return qs

