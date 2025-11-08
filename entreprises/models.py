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

    def __str__(self) -> str:
        return self.name

