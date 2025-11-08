from __future__ import annotations

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Departement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=16, unique=True, verbose_name="Code")),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="Nom")),
            ],
            options={
                "verbose_name": "Département",
                "verbose_name_plural": "Départements",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("action", models.CharField(max_length=255, verbose_name="Action")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                ("occurred_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date")),
                ("metadata", models.JSONField(blank=True, default=dict, verbose_name="Métadonnées")),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="audit_logs",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Utilisateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "Journal d'audit",
                "verbose_name_plural": "Journaux d'audit",
                "ordering": ("-occurred_at",),
            },
        ),
        migrations.CreateModel(
            name="Programme",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=32, verbose_name="Code")),
                ("title", models.CharField(max_length=255, verbose_name="Intitulé")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                (
                    "departement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="programmes",
                        to="core.departement",
                        verbose_name="Département",
                    ),
                ),
            ],
            options={
                "verbose_name": "Programme",
                "verbose_name_plural": "Programmes",
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Promotion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("year", models.PositiveIntegerField(verbose_name="Année de promotion")),
                ("start_date", models.DateField(verbose_name="Date de début")),
                ("end_date", models.DateField(verbose_name="Date de fin")),
                ("label", models.CharField(max_length=255, verbose_name="Libellé")),
                (
                    "programme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="promotions",
                        to="core.programme",
                        verbose_name="Programme",
                    ),
                ),
            ],
            options={
                "verbose_name": "Promotion",
                "verbose_name_plural": "Promotions",
                "ordering": ("-year", "programme__title"),
            },
        ),
        migrations.AddIndex(
            model_name="departement",
            index=models.Index(fields=["code"], name="core_departe_code_272eed_idx"),
        ),
        migrations.AddIndex(
            model_name="departement",
            index=models.Index(fields=["name"], name="core_departe_name_473ddf_idx"),
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["occurred_at"], name="core_auditl_occurre_43e90b_idx"),
        ),
        migrations.AddIndex(
            model_name="programme",
            index=models.Index(fields=["departement", "code"], name="core_program_departe_e4e479_idx"),
        ),
        migrations.AddConstraint(
            model_name="programme",
            constraint=models.UniqueConstraint(
                fields=("departement", "code"), name="programme_unique_code"
            ),
        ),
        migrations.AddIndex(
            model_name="promotion",
            index=models.Index(fields=["programme", "year"], name="core_promoti_program_0a76fd_idx"),
        ),
        migrations.AddIndex(
            model_name="promotion",
            index=models.Index(fields=["start_date", "end_date"], name="core_promoti_start_d_a072c5_idx"),
        ),
        migrations.AddConstraint(
            model_name="promotion",
            constraint=models.UniqueConstraint(
                fields=("programme", "year"), name="promotion_unique_programme_year"
            ),
        ),
    ]
