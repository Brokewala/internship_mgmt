from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import (
    AffectationViewSet,
    CandidatureViewSet,
    EntrepriseViewSet,
    LivrableViewSet,
    OffreStageViewSet,
)

router = DefaultRouter()
router.register("entreprises", EntrepriseViewSet, basename="entreprise")
router.register("offres", OffreStageViewSet, basename="offre-stage")
router.register("candidatures", CandidatureViewSet, basename="candidature")
router.register("affectations", AffectationViewSet, basename="affectation")
router.register("livrables", LivrableViewSet, basename="livrable")

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
