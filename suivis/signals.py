from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from evaluations.models import NoteFinale

from .models import Livrable


@receiver(post_save, sender=Livrable)
def livrable_post_save(sender, instance: Livrable, created: bool, **kwargs) -> None:
    note_finale, _ = NoteFinale.objects.get_or_create(affectation=instance.affectation)
    note_finale.refresh_score()
