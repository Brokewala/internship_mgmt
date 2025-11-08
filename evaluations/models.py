from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class BaseEvaluation(TimeStampedModel):
    affectation = models.ForeignKey(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        verbose_name=_("Affectation"),
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Évaluateur"),
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Note"))
    feedback = models.TextField(blank=True, verbose_name=_("Retour"))
    evaluation_date = models.DateField(verbose_name=_("Date d'évaluation"))

    class Meta:
        abstract = True
        ordering = ("-evaluation_date",)

    def clean(self) -> None:
        super().clean()
        if self.score < 0 or self.score > 20:
            raise ValidationError(_("La note doit être comprise entre 0 et 20."))


class EvaluationTuteurEntreprise(BaseEvaluation):
    affectation = models.OneToOneField(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        related_name="evaluation_entreprise",
        verbose_name=_("Affectation"),
    )

    class Meta(BaseEvaluation.Meta):
        verbose_name = _("Évaluation tuteur entreprise")
        verbose_name_plural = _("Évaluations tuteur entreprise")
        indexes = [models.Index(fields=["evaluation_date"])]

    def __str__(self) -> str:
        return f"Éval. entreprise {self.score}/20 - {self.affectation}"


class EvaluationTuteurEcole(BaseEvaluation):
    affectation = models.OneToOneField(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        related_name="evaluation_ecole",
        verbose_name=_("Affectation"),
    )

    class Meta(BaseEvaluation.Meta):
        verbose_name = _("Évaluation tuteur école")
        verbose_name_plural = _("Évaluations tuteur école")
        indexes = [models.Index(fields=["evaluation_date"])]

    def __str__(self) -> str:
        return f"Éval. école {self.score}/20 - {self.affectation}"


class NoteFinale(TimeStampedModel):
    affectation = models.OneToOneField(
        "affectations.Affectation",
        on_delete=models.CASCADE,
        related_name="note_finale",
        verbose_name=_("Affectation"),
    )
    coefficient_entreprise = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("0.4"),
        verbose_name=_("Coef. entreprise"),
    )
    coefficient_ecole = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("0.4"),
        verbose_name=_("Coef. école"),
    )
    coefficient_livrables = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("0.2"),
        verbose_name=_("Coef. livrables"),
    )
    valeur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Note finale"),
    )

    class Meta:
        verbose_name = _("Note finale")
        verbose_name_plural = _("Notes finales")
        indexes = [models.Index(fields=["valeur"])]

    def __str__(self) -> str:
        return f"Note finale {self.valeur}/20 - {self.affectation}"

    @property
    def note_finale(self) -> Decimal:
        return self.calculate_score()

    def calculate_score(self) -> Decimal:
        try:
            entreprise_score = self.affectation.evaluation_entreprise.score
        except ObjectDoesNotExist:
            entreprise_score = Decimal("0")
        try:
            ecole_score = self.affectation.evaluation_ecole.score
        except ObjectDoesNotExist:
            ecole_score = Decimal("0")
        livrables_score = (
            self.affectation.livrables.filter(score__isnull=False).aggregate(avg=Avg("score"))["avg"]
            or Decimal("0")
        )
        total_coef = (
            self.coefficient_entreprise + self.coefficient_ecole + self.coefficient_livrables
        ) or Decimal("1")
        final_score = (
            entreprise_score * self.coefficient_entreprise
            + ecole_score * self.coefficient_ecole
            + Decimal(str(livrables_score)) * self.coefficient_livrables
        ) / total_coef
        return final_score.quantize(Decimal("0.01"))

    def refresh_score(self, save: bool = True) -> Decimal:
        self.valeur = self.calculate_score()
        if save:
            self.save(update_fields=["valeur", "updated_at"])
        return self.valeur

