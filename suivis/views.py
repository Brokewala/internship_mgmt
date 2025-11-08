from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Suivi


class SuiviListView(LoginRequiredMixin, ListView):
    model = Suivi
    template_name = "suivis/suivi_list.html"
    context_object_name = "suivis"

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(affectation__student=self.request.user)
        return qs

