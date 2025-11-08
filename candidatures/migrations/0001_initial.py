from __future__ import annotations

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("offres", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Candidature",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Brouillon"),
                            ("SUBMITTED", "Soumise"),
                            ("ACCEPTED", "Acceptée"),
                            ("REJECTED", "Refusée"),
                        ],
                        default="SUBMITTED",
                        max_length=32,
                        verbose_name="Statut",
                    ),
                ),
                ("motivation", models.TextField(blank=True, verbose_name="Motivation")),
                (
                    "offer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to="offres.offrestage",
                        verbose_name="Offre",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidatures",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Étudiant",
                    ),
                ),
            ],
            options={
                "verbose_name": "Candidature",
                "verbose_name_plural": "Candidatures",
            },
        ),
        migrations.AddIndex(
            model_name="candidature",
            index=models.Index(fields=["status", "created_at"], name="candidat_status__e1f9f7_idx"),
        ),
        migrations.AddIndex(
            model_name="candidature",
            index=models.Index(fields=["offer", "status"], name="candidat_offer_id_70c9b6_idx"),
        ),
        migrations.AddConstraint(
            model_name="candidature",
            constraint=models.UniqueConstraint(
                fields=("student", "offer"), name="unique_application_per_student_offer"
            ),
        ),
    ]
