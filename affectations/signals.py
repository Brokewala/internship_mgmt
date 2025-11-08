from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Alerte
from evaluations.models import NoteFinale

from .models import Affectation


@receiver(post_save, sender=Affectation)
def create_affectation_alert(sender, instance: Affectation, created: bool, **kwargs) -> None:
    if created:
        Alerte.objects.create(
            titre="Nouvelle affectation",
            message=f"Une nouvelle affectation a été créée pour {instance.student}.",
            niveau=Alerte.Niveau.INFO,
            affectation=instance,
        )
        NoteFinale.objects.get_or_create(affectation=instance)
