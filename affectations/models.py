from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Affectation(TimeStampedModel):
    class Status(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", _("En attente")
        VALIDE = "VALIDE", _("Validée")
        EN_COURS = "EN_COURS", _("En cours")
        TERMINE = "TERMINE", _("Terminée")
        ANNULE = "ANNULE", _("Annulée")

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
        default=Status.EN_ATTENTE,
        verbose_name=_("Statut"),
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Affectation")
        verbose_name_plural = _("Affectations")
        ordering = ("-start_date",)
        indexes = [
            models.Index(fields=["status", "start_date"]),
            models.Index(fields=["entreprise", "status"]),
        ]

    def clean(self) -> None:
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("La date de fin doit être postérieure à la date de début."))
        if self.offer:
            if self.start_date and self.offer.start_date and self.start_date < self.offer.start_date:
                raise ValidationError(_("La date de début doit respecter celle de l'offre."))
            if self.end_date and self.offer.end_date and self.end_date > self.offer.end_date:
                raise ValidationError(_("La date de fin doit respecter celle de l'offre."))

    def __str__(self) -> str:
        return f"Affectation de {self.student} chez {self.entreprise} ({self.get_status_display()})"

