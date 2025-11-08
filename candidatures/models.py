from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Candidature(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Brouillon")
        SUBMITTED = "SUBMITTED", _("Soumise")
        INTERVIEW = "INTERVIEW", _("Entretien")
        ACCEPTED = "ACCEPTED", _("Acceptée")
        REJECTED = "REJECTED", _("Refusée")

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidatures",
        verbose_name=_("Étudiant"),
    )
    offer = models.ForeignKey(
        "offres.OffreStage",
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name=_("Offre"),
    )
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.SUBMITTED,
        verbose_name=_("Statut"),
    )
    motivation = models.TextField(blank=True, verbose_name=_("Motivation"))

    class Meta:
        verbose_name = _("Candidature")
        verbose_name_plural = _("Candidatures")
        unique_together = ("student", "offer")

    def __str__(self) -> str:
        return f"{self.student} -> {self.offer}"

