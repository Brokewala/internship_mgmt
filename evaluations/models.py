from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Evaluation(TimeStampedModel):
    affectation = models.ForeignKey(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        related_name="evaluations",
        verbose_name=_("Affectation"),
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evaluations_realisees",
        verbose_name=_("Évaluateur"),
    )
    rating = models.PositiveSmallIntegerField(verbose_name=_("Note"))
    feedback = models.TextField(verbose_name=_("Retour"))

    class Meta:
        verbose_name = _("Évaluation")
        verbose_name_plural = _("Évaluations")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Évaluation {self.rating}/5 pour {self.affectation}"

