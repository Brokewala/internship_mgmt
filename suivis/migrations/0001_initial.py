from __future__ import annotations

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("affectations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Suivi",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("meeting_date", models.DateField(verbose_name="Date de suivi")),
                ("summary", models.TextField(verbose_name="Résumé")),
                ("next_steps", models.TextField(blank=True, verbose_name="Prochaines étapes")),
                (
                    "affectation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="suivis",
                        to="affectations.affectation",
                        verbose_name="Affectation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Suivi",
                "verbose_name_plural": "Suivis",
                "ordering": ("-meeting_date",),
            },
        ),
        migrations.CreateModel(
            name="Journal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("entry_date", models.DateField(verbose_name="Date d'entrée")),
                ("content", models.TextField(verbose_name="Contenu")),
                (
                    "affectation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="journaux",
                        to="affectations.affectation",
                        verbose_name="Affectation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Journal",
                "verbose_name_plural": "Journaux",
                "ordering": ("-entry_date",),
            },
        ),
        migrations.CreateModel(
            name="Livrable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("RAPPORT", "Rapport"),
                            ("PRESENTATION", "Présentation"),
                            ("FICHE_EVAL", "Fiche d'évaluation"),
                        ],
                        max_length=32,
                        verbose_name="Type",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Titre")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                ("due_date", models.DateField(verbose_name="Date d'échéance")),
                ("submitted_at", models.DateField(blank=True, null=True, verbose_name="Date de remise")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("A_REMETTRE", "À remettre"),
                            ("EN_COURS", "En cours"),
                            ("SOUMIS", "Soumis"),
                            ("VALIDE", "Validé"),
                            ("REFUSE", "Refusé"),
                        ],
                        default="A_REMETTRE",
                        max_length=32,
                        verbose_name="Statut",
                    ),
                ),
                ("score", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Note")),
                (
                    "affectation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="livrables",
                        to="affectations.affectation",
                        verbose_name="Affectation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Livrable",
                "verbose_name_plural": "Livrables",
                "ordering": ("-due_date",),
            },
        ),
        migrations.AddIndex(
            model_name="journal",
            index=models.Index(fields=["entry_date"], name="suivis_jour_entry_d_aa91f5_idx"),
        ),
        migrations.AddIndex(
            model_name="livrable",
            index=models.Index(fields=["affectation", "type"], name="suivis_livr_affecta_128701_idx"),
        ),
        migrations.AddIndex(
            model_name="livrable",
            index=models.Index(fields=["status"], name="suivis_livr_status__e600f1_idx"),
        ),
        migrations.AddConstraint(
            model_name="livrable",
            constraint=models.UniqueConstraint(
                fields=("affectation", "type"), name="livrable_unique_type_affectation"
            ),
        ),
    ]
