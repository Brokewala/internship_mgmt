from __future__ import annotations

import importlib
from typing import Any

from affectations.models import Affectation


PDF_TEMPLATE = """
<html>
  <body>
    <h1>Convention de stage</h1>
    <p>Étudiant : {student}</p>
    <p>Entreprise : {entreprise}</p>
    <p>Période : du {start} au {end}</p>
  </body>
</html>
"""


def _get_weasyprint_html() -> Any:
    spec = importlib.util.find_spec("weasyprint")
    if spec is None:
        raise RuntimeError("WeasyPrint doit être installé pour générer les conventions de stage.")
    module = importlib.import_module("weasyprint")
    return getattr(module, "HTML")


def generate_convention_pdf(affectation: Affectation) -> bytes:
    html_renderer = _get_weasyprint_html()
    html = PDF_TEMPLATE.format(
        student=affectation.student,
        entreprise=affectation.entreprise,
        start=affectation.start_date.strftime("%d/%m/%Y"),
        end=affectation.end_date.strftime("%d/%m/%Y"),
    )
    return html_renderer(string=html).write_pdf()
