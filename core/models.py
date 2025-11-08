from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Departement(TimeStampedModel):
    code = models.CharField(max_length=16, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Nom"))

    class Meta:
        verbose_name = _("Département")
        verbose_name_plural = _("Départements")
        ordering = ("name",)
        indexes = [models.Index(fields=["code"]), models.Index(fields=["name"])]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Programme(TimeStampedModel):
    departement = models.ForeignKey(
        "core.Departement",
        on_delete=models.CASCADE,
        related_name="programmes",
        verbose_name=_("Département"),
    )
    code = models.CharField(max_length=32, verbose_name=_("Code"))
    title = models.CharField(max_length=255, verbose_name=_("Intitulé"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Programme")
        verbose_name_plural = _("Programmes")
        ordering = ("title",)
        indexes = [models.Index(fields=["departement", "code"])]
        constraints = [
            models.UniqueConstraint(
                fields=["departement", "code"],
                name="programme_unique_code",
            )
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.code})"


class Promotion(TimeStampedModel):
    programme = models.ForeignKey(
        "core.Programme",
        on_delete=models.CASCADE,
        related_name="promotions",
        verbose_name=_("Programme"),
    )
    year = models.PositiveIntegerField(verbose_name=_("Année de promotion"))
    start_date = models.DateField(verbose_name=_("Date de début"))
    end_date = models.DateField(verbose_name=_("Date de fin"))
    label = models.CharField(max_length=255, verbose_name=_("Libellé"))

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")
        ordering = ("-year", "programme__title")
        indexes = [
            models.Index(fields=["programme", "year"]),
            models.Index(fields=["start_date", "end_date"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["programme", "year"],
                name="promotion_unique_programme_year",
            )
        ]

    def clean(self) -> None:
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("La date de fin doit être postérieure au début."))

    def __str__(self) -> str:
        return f"{self.label} - {self.year}"


class Alerte(TimeStampedModel):
    class Niveau(models.TextChoices):
        INFO = "INFO", _("Information")
        WARNING = "WARNING", _("Avertissement")
        CRITICAL = "CRITICAL", _("Critique")

    titre = models.CharField(max_length=255, verbose_name=_("Titre"))
    message = models.TextField(verbose_name=_("Message"))
    niveau = models.CharField(
        max_length=16,
        choices=Niveau.choices,
        default=Niveau.INFO,
        verbose_name=_("Niveau"),
    )
    affectation = models.ForeignKey(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        related_name="alertes",
        null=True,
        blank=True,
        verbose_name=_("Affectation associée"),
    )
    resolue = models.BooleanField(default=False, verbose_name=_("Résolue"))

    class Meta:
        verbose_name = _("Alerte")
        verbose_name_plural = _("Alertes")
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["niveau", "resolue"])]

    def __str__(self) -> str:
        cible = f" pour {self.affectation}" if self.affectation else ""
        return f"[{self.get_niveau_display()}] {self.titre}{cible}"


class AuditLog(TimeStampedModel):
    action = models.CharField(max_length=255, verbose_name=_("Action"))
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name=_("Utilisateur"),
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    occurred_at = models.DateTimeField(default=timezone.now, verbose_name=_("Date"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Métadonnées"))

    class Meta:
        verbose_name = _("Journal d'audit")
        verbose_name_plural = _("Journaux d'audit")
        ordering = ("-occurred_at",)
        indexes = [models.Index(fields=["occurred_at"])]

    def __str__(self) -> str:
        user = self.actor if self.actor else _("Système")
        return f"{self.action} - {user} ({self.occurred_at:%d/%m/%Y %H:%M})"

