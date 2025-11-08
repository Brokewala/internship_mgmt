from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Affectation(TimeStampedModel):
    class Status(models.TextChoices):
        PLANNED = "PLANNED", _("Planifiée")
        ONGOING = "ONGOING", _("En cours")
        COMPLETED = "COMPLETED", _("Terminée")
        CANCELLED = "CANCELLED", _("Annulée")

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="affectations",
        verbose_name=_("Étudiant"),
    )
    offer = models.ForeignKey(
        "offres.OffreStage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affectations",
        verbose_name=_("Offre"),
    )
    entreprise = models.ForeignKey(
        "entreprises.Entreprise",
        on_delete=models.CASCADE,
        related_name="affectations",
        verbose_name=_("Entreprise"),
    )
    start_date = models.DateField(verbose_name=_("Date de début"))
    end_date = models.DateField(verbose_name=_("Date de fin"))
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name=_("Statut"),
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Affectation")
        verbose_name_plural = _("Affectations")
        ordering = ("-start_date",)

    def __str__(self) -> str:
        return f"{self.student} - {self.entreprise} ({self.get_status_display()})"

