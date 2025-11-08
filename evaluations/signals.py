from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EvaluationTuteurEcole, EvaluationTuteurEntreprise, NoteFinale


@receiver(post_save, sender=EvaluationTuteurEntreprise)
@receiver(post_save, sender=EvaluationTuteurEcole)
def evaluation_saved(sender, instance, **kwargs) -> None:
    note_finale, _ = NoteFinale.objects.get_or_create(affectation=instance.affectation)
    note_finale.refresh_score()
