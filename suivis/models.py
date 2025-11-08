from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Suivi(TimeStampedModel):
    affectation = models.ForeignKey(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        related_name="suivis",
        verbose_name=_("Affectation"),
    )
    meeting_date = models.DateField(verbose_name=_("Date de suivi"))
    summary = models.TextField(verbose_name=_("Résumé"))
    next_steps = models.TextField(blank=True, verbose_name=_("Prochaines étapes"))

    class Meta:
        verbose_name = _("Suivi")
        verbose_name_plural = _("Suivis")
        ordering = ("-meeting_date",)

    def __str__(self) -> str:
        return f"Suivi du {self.meeting_date} pour {self.affectation}"

