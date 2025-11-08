from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Entreprise(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("Nom"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Adresse"))
    website = models.URLField(blank=True, verbose_name=_("Site web"))
    contact_email = models.EmailField(blank=True, verbose_name=_("Email de contact"))

    class Meta:
        verbose_name = _("Entreprise")
        verbose_name_plural = _("Entreprises")
        ordering = ("name",)
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["contact_email"]),
        ]

    def __str__(self) -> str:
        return self.name


class ContactEntreprise(TimeStampedModel):
    entreprise = models.ForeignKey(
        "entreprises.Entreprise",
        on_delete=models.CASCADE,
        related_name="contacts",
        verbose_name=_("Entreprise"),
    )
    first_name = models.CharField(max_length=150, verbose_name=_("Prénom"))
    last_name = models.CharField(max_length=150, verbose_name=_("Nom"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_("Téléphone"))
    role = models.CharField(max_length=150, blank=True, verbose_name=_("Fonction"))

    class Meta:
        verbose_name = _("Contact d'entreprise")
        verbose_name_plural = _("Contacts d'entreprise")
        ordering = ("last_name", "first_name")
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.entreprise.name})"

