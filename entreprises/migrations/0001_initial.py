from __future__ import annotations

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Entreprise",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="Nom")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                ("address", models.CharField(blank=True, max_length=255, verbose_name="Adresse")),
                ("website", models.URLField(blank=True, verbose_name="Site web")),
                ("contact_email", models.EmailField(blank=True, max_length=254, verbose_name="Email de contact")),
            ],
            options={
                "verbose_name": "Entreprise",
                "verbose_name_plural": "Entreprises",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ContactEntreprise",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=150, verbose_name="Prénom")),
                ("last_name", models.CharField(max_length=150, verbose_name="Nom")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("phone", models.CharField(blank=True, max_length=50, verbose_name="Téléphone")),
                ("role", models.CharField(blank=True, max_length=150, verbose_name="Fonction")),
                (
                    "entreprise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="entreprises.entreprise",
                        verbose_name="Entreprise",
                    ),
                ),
            ],
            options={
                "verbose_name": "Contact d'entreprise",
                "verbose_name_plural": "Contacts d'entreprise",
                "ordering": ("last_name", "first_name"),
            },
        ),
        migrations.AddIndex(
            model_name="entreprise",
            index=models.Index(fields=["name"], name="entreprises_name_894421_idx"),
        ),
        migrations.AddIndex(
            model_name="entreprise",
            index=models.Index(fields=["contact_email"], name="entreprises_contact__a76aac_idx"),
        ),
        migrations.AddIndex(
            model_name="contactentreprise",
            index=models.Index(fields=["last_name", "first_name"], name="entreprise_last_na_3c5f47_idx"),
        ),
        migrations.AddIndex(
            model_name="contactentreprise",
            index=models.Index(fields=["email"], name="entreprise_email_13e9c2_idx"),
        ),
    ]
