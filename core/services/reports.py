from __future__ import annotations

import csv
from io import StringIO
from typing import Iterable

from affectations.models import Affectation
from offres.models import Campagne


CSV_HEADERS = [
    "Campagne",
    "Étudiant",
    "Entreprise",
    "Date de début",
    "Date de fin",
    "Statut",
]


def _format_student(affectation: Affectation) -> str:
    student = affectation.student
    return student.get_full_name() or student.get_username()


def export_assignments_by_campaign(
    campagne: Campagne | None = None,
    queryset: Iterable[Affectation] | None = None,
) -> str:
    assignments = queryset or Affectation.objects.select_related(
        "student", "entreprise", "offer__campagne"
    )
    if campagne is not None:
        assignments = assignments.filter(offer__campagne=campagne)

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(CSV_HEADERS)

    for affectation in assignments.order_by("offer__campagne__title", "student__last_name"):
        campagne_title = "Sans campagne"
        if affectation.offer and affectation.offer.campagne:
            campagne_title = affectation.offer.campagne.title
        writer.writerow(
            [
                campagne_title,
                _format_student(affectation),
                affectation.entreprise.name,
                affectation.start_date.strftime("%d/%m/%Y"),
                affectation.end_date.strftime("%d/%m/%Y"),
                affectation.get_status_display(),
            ]
        )

    return buffer.getvalue()
