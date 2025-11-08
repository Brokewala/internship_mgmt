from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Entreprise


class EntrepriseListView(LoginRequiredMixin, ListView):
    model = Entreprise
    template_name = "entreprises/entreprise_list.html"
    context_object_name = "entreprises"

