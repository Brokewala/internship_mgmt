from __future__ import annotations

from django.core.exceptions import ValidationError
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


class Journal(TimeStampedModel):
    affectation = models.ForeignKey(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        related_name="journaux",
        verbose_name=_("Affectation"),
    )
    entry_date = models.DateField(verbose_name=_("Date d'entrée"))
    content = models.TextField(verbose_name=_("Contenu"))

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journaux")
        ordering = ("-entry_date",)
        indexes = [models.Index(fields=["entry_date"])]

    def clean(self) -> None:
        super().clean()
        affectation = self.affectation
        if affectation and affectation.start_date and self.entry_date < affectation.start_date:
            raise ValidationError(_("La date du journal ne peut pas précéder le début de l'affectation."))
        if affectation and affectation.end_date and self.entry_date > affectation.end_date:
            raise ValidationError(_("La date du journal ne peut pas dépasser la fin de l'affectation."))

    def __str__(self) -> str:
        return f"Journal du {self.entry_date:%d/%m/%Y} - {self.affectation}"


class Livrable(TimeStampedModel):
    class Type(models.TextChoices):
        RAPPORT = "RAPPORT", _("Rapport")
        PRESENTATION = "PRESENTATION", _("Présentation")
        FICHE_EVAL = "FICHE_EVAL", _("Fiche d'évaluation")

    class Status(models.TextChoices):
        A_REMETTRE = "A_REMETTRE", _("À remettre")
        EN_COURS = "EN_COURS", _("En cours")
        SOUMIS = "SOUMIS", _("Soumis")
        VALIDE = "VALIDE", _("Validé")
        REFUSE = "REFUSE", _("Refusé")

    affectation = models.ForeignKey(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        related_name="livrables",
        verbose_name=_("Affectation"),
    )
    type = models.CharField(max_length=32, choices=Type.choices, verbose_name=_("Type"))
    title = models.CharField(max_length=255, verbose_name=_("Titre"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    due_date = models.DateField(verbose_name=_("Date d'échéance"))
    submitted_at = models.DateField(blank=True, null=True, verbose_name=_("Date de remise"))
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.A_REMETTRE,
        verbose_name=_("Statut"),
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Note"),
    )

    class Meta:
        verbose_name = _("Livrable")
        verbose_name_plural = _("Livrables")
        ordering = ("-due_date",)
        indexes = [
            models.Index(fields=["affectation", "type"]),
            models.Index(fields=["status"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["affectation", "type"],
                name="livrable_unique_type_affectation",
            )
        ]

    def clean(self) -> None:
        super().clean()
        if self.submitted_at and self.submitted_at < self.due_date:
            raise ValidationError(_("La date de remise ne peut pas précéder l'échéance."))
        if self.affectation:
            if self.due_date and self.affectation.start_date and self.due_date < self.affectation.start_date:
                raise ValidationError(_("L'échéance doit être postérieure au début de l'affectation."))
            if self.affectation.end_date and self.due_date > self.affectation.end_date:
                raise ValidationError(_("L'échéance doit être avant la fin de l'affectation."))

    def __str__(self) -> str:
        return f"{self.get_type_display()} - {self.affectation}"

