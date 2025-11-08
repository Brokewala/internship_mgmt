from __future__ import annotations

import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from affectations.models import Affectation
from candidatures.models import Candidature
from entreprises.models import Entreprise
from evaluations.models import Evaluation
from offres.models import OffreStage
from reporting.models import ReportSnapshot
from suivis.models import Suivi

try:
    from faker import Faker
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise ImportError(
        "Faker doit être installé pour utiliser cette commande. Ajoutez-le à vos dépendances."
    ) from exc


class Command(BaseCommand):
    help = "Crée un jeu de données de démonstration pour le portail stages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Supprime les données existantes liées avant d'insérer les données de démonstration.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options.get("force", False)
        faker = Faker("fr_FR")
        Faker.seed(42)
        random.seed(42)

        User = get_user_model()

        if not force and Entreprise.objects.exists():
            self.stdout.write(self.style.WARNING("Des données existent déjà. Utilisez --force pour écraser."))
            return

        self.stdout.write(self.style.MIGRATE_HEADING("Nettoyage des données précédentes..."))
        Candidature.objects.all().delete()
        Affectation.objects.all().delete()
        Suivi.objects.all().delete()
        Evaluation.objects.all().delete()
        OffreStage.objects.all().delete()
        Entreprise.objects.all().delete()
        ReportSnapshot.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS("Création des entreprises"))
        entreprises = []
        for _ in range(10):
            entreprise = Entreprise.objects.create(
                name=faker.company(),
                description=faker.catch_phrase(),
                address=faker.address().replace("\n", ", "),
                website=faker.url(),
                contact_email=faker.company_email(),
            )
            entreprises.append(entreprise)

        self.stdout.write(self.style.SUCCESS("Création des étudiants"))
        students = []
        for index in range(50):
            first_name = faker.first_name()
            last_name = faker.last_name()
            username = f"etudiant{index+1:02d}"
            student = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="Passw0rd!",
                first_name=first_name,
                last_name=last_name,
                role=User.Roles.STUDENT,
            )
            student.profile.bio = faker.text(max_nb_chars=120)
            student.profile.linkedin_url = faker.url()
            student.profile.save()
            students.append(student)

        self.stdout.write(self.style.SUCCESS("Création des offres"))
        offers = []
        base_date = timezone.now().date()
        for index in range(20):
            entreprise = random.choice(entreprises)
            start = base_date + timedelta(days=random.randint(15, 90))
            end = start + timedelta(days=90)
            offer = OffreStage.objects.create(
                entreprise=entreprise,
                title=f"Stage {faker.job()} #{index+1}",
                description=faker.paragraph(nb_sentences=5),
                location=faker.city(),
                start_date=start,
                end_date=end,
                slots=random.randint(1, 3),
                status=OffreStage.Status.PUBLISHED,
            )
            offers.append(offer)

        self.stdout.write(self.style.SUCCESS("Création des candidatures"))
        candidatures = []
        for _ in range(40):
            student = random.choice(students)
            offer = random.choice(offers)
            candidature, _ = Candidature.objects.get_or_create(
                student=student,
                offer=offer,
                defaults={
                    "status": random.choice(list(Candidature.Status.values)),
                    "motivation": faker.paragraph(nb_sentences=3),
                },
            )
            candidatures.append(candidature)

        self.stdout.write(self.style.SUCCESS("Création des affectations"))
        affectations = []
        for candidature in random.sample(candidatures, k=min(25, len(candidatures))):
            start = candidature.offer.start_date
            affectation = Affectation.objects.create(
                student=candidature.student,
                offer=candidature.offer,
                entreprise=candidature.offer.entreprise,
                start_date=start,
                end_date=candidature.offer.end_date,
                status=random.choice(list(Affectation.Status.values)),
                notes=faker.text(max_nb_chars=200),
            )
            affectations.append(affectation)

        self.stdout.write(self.style.SUCCESS("Ajout des suivis et évaluations"))
        for affectation in affectations:
            for _ in range(random.randint(1, 3)):
                Suivi.objects.create(
                    affectation=affectation,
                    meeting_date=affectation.start_date + timedelta(days=random.randint(7, 45)),
                    summary=faker.sentence(nb_words=12),
                    next_steps=faker.sentence(nb_words=10),
                )
            Evaluation.objects.create(
                affectation=affectation,
                evaluator=random.choice(students),
                rating=random.randint(3, 5),
                feedback=faker.paragraph(nb_sentences=4),
            )

        self.stdout.write(self.style.SUCCESS("Création d'un instantané de reporting"))
        ReportSnapshot.objects.create(
            total_students=len(students),
            total_offers=len(offers),
            total_assignments=len(affectations),
            metadata={
                "generated_by": "seed_demo_data",
                "timestamp": timezone.now().isoformat(),
            },
        )

        self.stdout.write(self.style.SUCCESS("Jeu de données de démonstration créé avec succès."))

