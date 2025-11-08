from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", _("Administrateur")
        STAFF = "STAFF", _("Personnel")
        SUPERVISOR = "SUPERVISOR", _("Tuteur entreprise")
        STUDENT = "STUDENT", _("Étudiant")

    role = models.CharField(
        max_length=32,
        choices=Roles.choices,
        default=Roles.STUDENT,
        help_text=_("Détermine les permissions applicatives de l'utilisateur."),
    )
    phone_number = models.CharField(
        max_length=32,
        blank=True,
        help_text=_("Numéro de téléphone professionnel ou personnel."),
    )
    organisation = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Organisation à laquelle l'utilisateur est rattaché."),
    )

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Utilisateur"),
    )
    bio = models.TextField(blank=True, verbose_name=_("Biographie"))
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")
    portfolio_url = models.URLField(blank=True, verbose_name=_("Portfolio"))

    class Meta:
        verbose_name = _("Profil utilisateur")
        verbose_name_plural = _("Profils utilisateur")

    def __str__(self) -> str:
        return f"Profil de {self.user}"

