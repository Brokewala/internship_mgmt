from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from evaluations.models import NoteFinale

from .models import Affectation


@receiver(post_save, sender=Affectation)
def create_affectation_alert(sender, instance: Affectation, created: bool, **kwargs) -> None:
    if created:
        NoteFinale.objects.get_or_create(affectation=instance)
