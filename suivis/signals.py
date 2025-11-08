from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Alerte
from evaluations.models import NoteFinale

from .models import Livrable


@receiver(post_save, sender=Livrable)
def livrable_post_save(sender, instance: Livrable, created: bool, **kwargs) -> None:
    if created:
        Alerte.objects.create(
            titre=f"Nouveau livrable {instance.get_type_display()}",
            message=f"Un livrable de type {instance.get_type_display()} a été ajouté pour {instance.affectation}.",
            niveau=Alerte.Niveau.WARNING,
            affectation=instance.affectation,
        )

    note_finale, _ = NoteFinale.objects.get_or_create(affectation=instance.affectation)
    note_finale.refresh_score()
