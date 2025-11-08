from __future__ import annotations

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("affectations", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Alerte",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("titre", models.CharField(max_length=255, verbose_name="Titre")),
                ("message", models.TextField(verbose_name="Message")),
                (
                    "niveau",
                    models.CharField(
                        choices=[
                            ("INFO", "Information"),
                            ("WARNING", "Avertissement"),
                            ("CRITICAL", "Critique"),
                        ],
                        default="INFO",
                        max_length=16,
                        verbose_name="Niveau",
                    ),
                ),
                ("resolue", models.BooleanField(default=False, verbose_name="Résolue")),
                (
                    "affectation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alertes",
                        to="affectations.affectation",
                        verbose_name="Affectation associée",
                    ),
                ),
            ],
            options={
                "verbose_name": "Alerte",
                "verbose_name_plural": "Alertes",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddIndex(
            model_name="alerte",
            index=models.Index(fields=["niveau", "resolue"], name="core_alerte_niveau__363c6a_idx"),
        ),
    ]
