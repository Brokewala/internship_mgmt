from __future__ import annotations

from django import template
from django.apps import apps
from django.db.models import Count
from django.utils import timezone

register = template.Library()


@register.simple_tag
def dashboard_kpis() -> dict[str, int]:
    User = apps.get_model("accounts", "User")
    OffreStage = apps.get_model("offres", "OffreStage")
    Affectation = apps.get_model("affectations", "Affectation")
    Livrable = apps.get_model("suivis", "Livrable")

    today = timezone.now().date()

    active_offers = 0
    if OffreStage:
        active_offers = OffreStage.objects.filter(
            status=OffreStage.Status.PUBLISHED,
            end_date__gte=today,
        ).count()

    ongoing_assignments = 0
    placement_statuses = []
    if Affectation:
        placement_statuses = [
            Affectation.Status.VALIDE,
            Affectation.Status.EN_COURS,
            Affectation.Status.TERMINE,
        ]
        ongoing_assignments = Affectation.objects.filter(
            status__in=[Affectation.Status.VALIDE, Affectation.Status.EN_COURS]
        ).count()

    late_deliverables = 0
    if Livrable:
        late_deliverables = Livrable.objects.filter(
            due_date__lt=today,
            status__in=[Livrable.Status.A_REMETTRE, Livrable.Status.EN_COURS],
        ).count()

    placement_rate = 0
    if User and Affectation:
        total_students = User.objects.filter(role=User.Roles.STUDENT).count()
        if total_students:
            placed_students = (
                Affectation.objects.filter(status__in=placement_statuses)
                .values_list("student_id", flat=True)
                .distinct()
                .count()
            )
            placement_rate = round((placed_students / total_students) * 100, 1)

    return {
        "active_offers": active_offers,
        "ongoing_assignments": ongoing_assignments,
        "late_deliverables": late_deliverables,
        "placement_rate": placement_rate,
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

