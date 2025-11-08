from __future__ import annotations

from datetime import date, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from suivis.models import Livrable

from .services.alerts import generate_deadline_alerts
from .services.emails import send_deadline_email
from .services.reports import export_assignments_by_campaign


def _get_upcoming_deliverables(reference_date: date) -> list[Livrable]:
    window_end = reference_date + timedelta(days=1)
    return list(
        Livrable.objects.select_related("affectation", "affectation__student")
        .filter(
            due_date__range=(reference_date, window_end),
            status__in=(Livrable.Status.A_REMETTRE, Livrable.Status.EN_COURS),
        )
        .order_by("due_date")
    )


@shared_task
def daily_deadline_reminders() -> dict[str, int]:
    reference_date = timezone.localdate()
    deliverables = _get_upcoming_deliverables(reference_date)
    emails_sent = 0
    for livrable in deliverables:
        emails_sent += send_deadline_email(livrable)
    alerts = generate_deadline_alerts(reference_date=reference_date)
    return {"emails_sent": emails_sent, "alerts_generated": len(alerts)}


@shared_task
def weekly_campaign_digest() -> dict[str, int]:
    csv_content = export_assignments_by_campaign()
    recipients = getattr(settings, "REPORTS_DIGEST_RECIPIENTS", [])
    emails_sent = 0
    if recipients:
        email = EmailMessage(
            subject="Digest hebdomadaire des affectations",
            body=(
                "Veuillez trouver en pièce jointe le récapitulatif hebdomadaire "
                "des affectations par campagne."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=list(recipients),
        )
        email.attach("digest_affectations.csv", csv_content, "text/csv")
        email.send(fail_silently=False)
        emails_sent = len(recipients)

    data_rows = max(len(csv_content.splitlines()) - 1, 0)
    return {"emails_sent": emails_sent, "rows_in_report": data_rows}
