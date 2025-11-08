from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Campagne(TimeStampedModel):
    promotion = models.ForeignKey(
        "core.Promotion",
        on_delete=models.CASCADE,
        related_name="campagnes",
        verbose_name=_("Promotion"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Titre"))
    start_date = models.DateField(verbose_name=_("Date de début"))
    end_date = models.DateField(verbose_name=_("Date de fin"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Campagne")
        verbose_name_plural = _("Campagnes")
        ordering = ("-start_date",)
        indexes = [models.Index(fields=["start_date", "end_date"])]
        constraints = [
            models.UniqueConstraint(
                fields=["promotion", "title"],
                name="campagne_unique_promotion_title",
            )
        ]

    def clean(self) -> None:
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("La date de fin doit être postérieure à la date de début."))

    def __str__(self) -> str:
        return f"{self.title} - {self.promotion}"


class OffreStage(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Brouillon")
        PUBLISHED = "PUBLISHED", _("Publiée")
        ARCHIVED = "ARCHIVED", _("Archivée")

    entreprise = models.ForeignKey(
        "entreprises.Entreprise",
        on_delete=models.CASCADE,
        related_name="offres",
        verbose_name=_("Entreprise"),
    )
    campagne = models.ForeignKey(
        "offres.Campagne",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offres",
        verbose_name=_("Campagne"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Titre"))
    description = models.TextField(verbose_name=_("Description"))
    location = models.CharField(max_length=255, verbose_name=_("Localisation"))
    start_date = models.DateField(verbose_name=_("Date de début"))
    end_date = models.DateField(verbose_name=_("Date de fin"))
    slots = models.PositiveIntegerField(default=1, verbose_name=_("Nombre de places"))
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name=_("Statut"),
    )

    class Meta:
        verbose_name = _("Offre de stage")
        verbose_name_plural = _("Offres de stage")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status", "start_date"]),
            models.Index(fields=["entreprise", "status"]),
        ]

    def clean(self) -> None:
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("La date de fin doit être postérieure à la date de début."))
        if self.campagne and (
            (self.start_date and self.campagne.start_date and self.start_date < self.campagne.start_date)
            or (self.end_date and self.campagne.end_date and self.end_date > self.campagne.end_date)
        ):
            raise ValidationError(
                _("Les dates de l'offre doivent être comprises dans la campagne associée."),
            )

    def __str__(self) -> str:
        return f"{self.title} ({self.entreprise.name})"

