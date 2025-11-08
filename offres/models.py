from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


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

    def __str__(self) -> str:
        return f"{self.title} - {self.entreprise.name}"

