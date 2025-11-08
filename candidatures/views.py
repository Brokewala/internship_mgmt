from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Candidature


class CandidatureListView(LoginRequiredMixin, ListView):
    model = Candidature
    template_name = "candidatures/candidature_list.html"
    context_object_name = "candidatures"

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(student=self.request.user)
        return qs

