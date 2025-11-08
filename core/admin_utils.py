from __future__ import annotations

import csv
import io
from typing import Iterable, Sequence

from django.http import HttpResponse


def build_csv_response(
    queryset,
    field_names: Sequence[str] | None = None,
    filename: str | None = None,
) -> HttpResponse:
    """Return a CSV HttpResponse for the provided queryset."""

    model = queryset.model
    if field_names is None:
        field_names = [field.name for field in model._meta.fields]
    filename = filename or f"{model._meta.model_name}_export.csv"

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(field_names)

    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        writer.writerow(row)

    response = HttpResponse(buffer.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def export_as_csv_action(
    modeladmin,
    request,
    queryset,
    field_names: Iterable[str] | None = None,
):
    return build_csv_response(queryset, tuple(field_names) if field_names else None)
