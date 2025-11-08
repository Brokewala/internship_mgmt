from __future__ import annotations

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
        ("entreprises", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campagne",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255, verbose_name="Titre")),
                ("start_date", models.DateField(verbose_name="Date de début")),
                ("end_date", models.DateField(verbose_name="Date de fin")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                (
                    "promotion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="campagnes",
                        to="core.promotion",
                        verbose_name="Promotion",
                    ),
                ),
            ],
            options={
                "verbose_name": "Campagne",
                "verbose_name_plural": "Campagnes",
                "ordering": ("-start_date",),
            },
        ),
        migrations.CreateModel(
            name="OffreStage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255, verbose_name="Titre")),
                ("description", models.TextField(verbose_name="Description")),
                ("location", models.CharField(max_length=255, verbose_name="Localisation")),
                ("start_date", models.DateField(verbose_name="Date de début")),
                ("end_date", models.DateField(verbose_name="Date de fin")),
                ("slots", models.PositiveIntegerField(default=1, verbose_name="Nombre de places")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Brouillon"),
                            ("PUBLISHED", "Publiée"),
                            ("ARCHIVED", "Archivée"),
                        ],
                        default="PUBLISHED",
                        max_length=32,
                        verbose_name="Statut",
                    ),
                ),
                (
                    "campagne",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="offres",
                        to="offres.campagne",
                        verbose_name="Campagne",
                    ),
                ),
                (
                    "entreprise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offres",
                        to="entreprises.entreprise",
                        verbose_name="Entreprise",
                    ),
                ),
            ],
            options={
                "verbose_name": "Offre de stage",
                "verbose_name_plural": "Offres de stage",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddIndex(
            model_name="campagne",
            index=models.Index(fields=["start_date", "end_date"], name="offres_camp_start_d_31aaae_idx"),
        ),
        migrations.AddConstraint(
            model_name="campagne",
            constraint=models.UniqueConstraint(
                fields=("promotion", "title"), name="campagne_unique_promotion_title"
            ),
        ),
        migrations.AddIndex(
            model_name="offrestage",
            index=models.Index(fields=["status", "start_date"], name="offres_offr_status_0b02b3_idx"),
        ),
        migrations.AddIndex(
            model_name="offrestage",
            index=models.Index(fields=["entreprise", "status"], name="offres_offr_entrepr_ae0100_idx"),
        ),
    ]
