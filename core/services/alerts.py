from __future__ import annotations

from datetime import date, timedelta
from typing import Iterable

from django.utils import timezone

from affectations.models import Affectation
from core.models import Alerte
from suivis.models import Livrable

LIVRABLE_ALERT_WINDOW_DAYS = 3
SOUTENANCE_ALERT_WINDOW_DAYS = 7


def _livrable_alert_message(livrable: Livrable) -> str:
    return (
        "Le livrable « {title} » est attendu pour le {due:%d/%m/%Y}. "
        "Merci de vérifier que l'étudiant a bien soumis les documents."
    ).format(title=livrable.title, due=livrable.due_date)


def _soutenance_alert_message(affectation: Affectation) -> str:
    return (
        "La soutenance pour {student} doit être planifiée au plus tard le {end:%d/%m/%Y}."
    ).format(student=affectation.student, end=affectation.end_date)


def generate_deadline_alerts(reference_date: date | None = None) -> list[Alerte]:
    today = reference_date or timezone.localdate()
    alerts: list[Alerte] = []

    livrables = Livrable.objects.select_related("affectation", "affectation__student").filter(
        due_date__range=(today, today + timedelta(days=LIVRABLE_ALERT_WINDOW_DAYS)),
        status__in=(Livrable.Status.A_REMETTRE, Livrable.Status.EN_COURS),
    )
    for livrable in livrables:
        alert, created = Alerte.objects.get_or_create(
            affectation=livrable.affectation,
            titre=f"Échéance livrable : {livrable.title}",
            defaults={
                "message": _livrable_alert_message(livrable),
                "niveau": Alerte.Niveau.WARNING,
            },
        )
        if created:
            alerts.append(alert)

    soutenances = Affectation.objects.select_related("student", "entreprise").filter(
        end_date__range=(today, today + timedelta(days=SOUTENANCE_ALERT_WINDOW_DAYS))
    )
    for affectation in soutenances:
        alert, created = Alerte.objects.get_or_create(
            affectation=affectation,
            titre="Soutenance à planifier",
            defaults={
                "message": _soutenance_alert_message(affectation),
                "niveau": Alerte.Niveau.INFO,
            },
        )
        if created:
            alerts.append(alert)

    return alerts


def summarize_alerts(alerts: Iterable[Alerte]) -> dict[str, int]:
    summary: dict[str, int] = {
        Alerte.Niveau.INFO: 0,
        Alerte.Niveau.WARNING: 0,
        Alerte.Niveau.CRITICAL: 0,
    }
    for alert in alerts:
        summary[alert.niveau] = summary.get(alert.niveau, 0) + 1
    return summary
