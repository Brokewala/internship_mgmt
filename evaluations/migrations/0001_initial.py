from __future__ import annotations

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("affectations", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NoteFinale",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("coefficient_entreprise", models.DecimalField(decimal_places=2, default="0.4", max_digits=4, verbose_name="Coef. entreprise")),
                ("coefficient_ecole", models.DecimalField(decimal_places=2, default="0.4", max_digits=4, verbose_name="Coef. école")),
                ("coefficient_livrables", models.DecimalField(decimal_places=2, default="0.2", max_digits=4, verbose_name="Coef. livrables")),
                ("valeur", models.DecimalField(decimal_places=2, default="0.00", max_digits=5, verbose_name="Note finale")),
                (
                    "affectation",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="note_finale",
                        to="affectations.affectation",
                        verbose_name="Affectation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Note finale",
                "verbose_name_plural": "Notes finales",
            },
        ),
        migrations.CreateModel(
            name="EvaluationTuteurEntreprise",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("score", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Note")),
                ("feedback", models.TextField(blank=True, verbose_name="Retour")),
                ("evaluation_date", models.DateField(verbose_name="Date d'évaluation")),
                (
                    "affectation",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluation_entreprise",
                        to="affectations.affectation",
                        verbose_name="Affectation",
                    ),
                ),
                (
                    "evaluator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Évaluateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "Évaluation tuteur entreprise",
                "verbose_name_plural": "Évaluations tuteur entreprise",
                "ordering": ("-evaluation_date",),
            },
        ),
        migrations.CreateModel(
            name="EvaluationTuteurEcole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("score", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Note")),
                ("feedback", models.TextField(blank=True, verbose_name="Retour")),
                ("evaluation_date", models.DateField(verbose_name="Date d'évaluation")),
                (
                    "affectation",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluation_ecole",
                        to="affectations.affectation",
                        verbose_name="Affectation",
                    ),
                ),
                (
                    "evaluator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Évaluateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "Évaluation tuteur école",
                "verbose_name_plural": "Évaluations tuteur école",
                "ordering": ("-evaluation_date",),
            },
        ),
        migrations.AddIndex(
            model_name="notefinale",
            index=models.Index(fields=["valeur"], name="evaluations_valeur_d78a55_idx"),
        ),
        migrations.AddIndex(
            model_name="evaluationtuteurentreprise",
            index=models.Index(fields=["evaluation_date"], name="evaluation_evaluati_4f7915_idx"),
        ),
        migrations.AddIndex(
            model_name="evaluationtuteurecole",
            index=models.Index(fields=["evaluation_date"], name="evaluation_evaluati_b50bce_idx"),
        ),
    ]
