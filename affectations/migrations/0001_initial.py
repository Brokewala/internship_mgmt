from __future__ import annotations

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("entreprises", "0001_initial"),
        ("offres", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Affectation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_date", models.DateField(verbose_name="Date de début")),
                ("end_date", models.DateField(verbose_name="Date de fin")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("EN_ATTENTE", "En attente"),
                            ("VALIDE", "Validée"),
                            ("EN_COURS", "En cours"),
                            ("TERMINE", "Terminée"),
                            ("ANNULE", "Annulée"),
                        ],
                        default="EN_ATTENTE",
                        max_length=32,
                        verbose_name="Statut",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="Notes")),
                (
                    "entreprise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="affectations",
                        to="entreprises.entreprise",
                        verbose_name="Entreprise",
                    ),
                ),
                (
                    "offer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="affectations",
                        to="offres.offrestage",
                        verbose_name="Offre",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="affectations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Étudiant",
                    ),
                ),
            ],
            options={
                "verbose_name": "Affectation",
                "verbose_name_plural": "Affectations",
                "ordering": ("-start_date",),
            },
        ),
        migrations.AddIndex(
            model_name="affectation",
            index=models.Index(fields=["status", "start_date"], name="affectatio_status__0614a8_idx"),
        ),
        migrations.AddIndex(
            model_name="affectation",
            index=models.Index(fields=["entreprise", "status"], name="affectatio_entrepri_99f0e7_idx"),
        ),
    ]
