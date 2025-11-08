from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class ReportSnapshot(TimeStampedModel):
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Généré le"))
    total_students = models.PositiveIntegerField(default=0, verbose_name=_("Total étudiants"))
    total_offers = models.PositiveIntegerField(default=0, verbose_name=_("Total offres"))
    total_assignments = models.PositiveIntegerField(default=0, verbose_name=_("Total affectations"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Métadonnées"))

    class Meta:
        verbose_name = _("Instantané de reporting")
        verbose_name_plural = _("Instantanés de reporting")
        ordering = ("-generated_at",)

    def __str__(self) -> str:
        return f"Reporting du {self.generated_at:%d/%m/%Y %H:%M}"

