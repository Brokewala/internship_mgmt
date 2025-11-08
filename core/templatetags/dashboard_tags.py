from __future__ import annotations

from django import template
from django.apps import apps
from django.db.models import Count

register = template.Library()


@register.simple_tag
def dashboard_kpis() -> dict[str, int]:
    User = apps.get_model("accounts", "User")
    OffreStage = apps.get_model("offres", "OffreStage")
    Candidature = apps.get_model("candidatures", "Candidature")
    Affectation = apps.get_model("affectations", "Affectation")

    total_users = User.objects.count() if User else 0
    total_students = User.objects.filter(role=User.Roles.STUDENT).count() if User else 0
    total_offers = OffreStage.objects.count() if OffreStage else 0
    total_applications = Candidature.objects.count() if Candidature else 0
    total_assignments = Affectation.objects.count() if Affectation else 0

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_offers": total_offers,
        "total_applications": total_applications,
        "total_assignments": total_assignments,
    }


@register.simple_tag
def top_offers(limit: int = 5):
    Candidature = apps.get_model("candidatures", "Candidature")
    OffreStage = apps.get_model("offres", "OffreStage")

    if not (Candidature and OffreStage):
        return []

    return (
        OffreStage.objects.annotate(applications=Count("applications"))
        .order_by("-applications")[:limit]
    )

