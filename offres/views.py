from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import OffreStage


class OffreListView(LoginRequiredMixin, ListView):
    model = OffreStage
    template_name = "offres/offre_list.html"
    context_object_name = "offres"

