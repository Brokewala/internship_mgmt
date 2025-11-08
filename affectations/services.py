from __future__ import annotations

import io
import zipfile
from typing import Iterable

from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils.text import slugify

from .models import Affectation


PLACEHOLDER_PDF_TEMPLATE = """%PDF-1.4\n1 0 obj<<>>endobj\n2 0 obj<<>>endobj\n3 0 obj<</Length 44>>stream\nConvention de stage pour {student}\nEntreprise : {entreprise}\nDates : {start} - {end}\nendstream\nendobj\n4 0 obj<</Type /Catalog /Pages 2 0 R>>endobj\ntrailer<</Root 4 0 R>>\n%%EOF\n"""


def generate_convention_pdf_content(affectation: Affectation) -> bytes:
    return PLACEHOLDER_PDF_TEMPLATE.format(
        student=str(affectation.student),
        entreprise=str(affectation.entreprise),
        start=affectation.start_date,
        end=affectation.end_date,
    ).encode("utf-8")


def build_conventions_archive(
    queryset: Iterable[Affectation] | QuerySet[Affectation],
) -> HttpResponse:
    affectations = list(queryset)
    archive_buffer = io.BytesIO()
    with zipfile.ZipFile(archive_buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for affectation in affectations:
            filename = f"convention-{slugify(str(affectation.student))}-{affectation.pk}.pdf"
            archive.writestr(filename, generate_convention_pdf_content(affectation))
    archive_buffer.seek(0)
    response = HttpResponse(archive_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=conventions.zip"
    return response
