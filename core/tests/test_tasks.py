from __future__ import annotations

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from affectations.models import Affectation
from core.models import Departement, Programme, Promotion
from core.tasks import daily_deadline_reminders, weekly_campaign_digest
from entreprises.models import Entreprise
from offres.models import Campagne, OffreStage
from suivis.models import Livrable


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class TaskTests(TestCase):
    def setUp(self) -> None:
        today = timezone.localdate()
        User = get_user_model()
        self.student = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password",
            first_name="Alice",
            last_name="Durand",
        )
        self.departement = Departement.objects.create(code="INFO", name="Informatique")
        self.programme = Programme.objects.create(
            departement=self.departement,
            code="DEV",
            title="Développement logiciel",
            description="",
        )
        self.promotion = Promotion.objects.create(
            programme=self.programme,
            year=today.year,
            start_date=today - timedelta(days=30),
            end_date=today + timedelta(days=365),
            label="Promo DEV",
        )
        self.campagne = Campagne.objects.create(
            promotion=self.promotion,
            title="Campagne Printemps",
            start_date=today - timedelta(days=10),
            end_date=today + timedelta(days=60),
            description="",
        )
        self.entreprise = Entreprise.objects.create(name="Tech Corp")
        self.offer = OffreStage.objects.create(
            entreprise=self.entreprise,
            campagne=self.campagne,
            title="Développeur stagiaire",
            description="",
            location="Paris",
            start_date=today,
            end_date=today + timedelta(days=120),
            slots=1,
        )
        self.affectation = Affectation.objects.create(
            student=self.student,
            offer=self.offer,
            entreprise=self.entreprise,
            start_date=today,
            end_date=today + timedelta(days=5),
            status=Affectation.Status.EN_COURS,
        )
        self.livrable = Livrable.objects.create(
            affectation=self.affectation,
            type=Livrable.Type.RAPPORT,
            title="Rapport intermédiaire",
            description="",
            due_date=today + timedelta(days=1),
            status=Livrable.Status.A_REMETTRE,
        )
        mail.outbox = []

    def test_daily_deadline_reminders_sends_emails_without_alerts(self) -> None:
        result = daily_deadline_reminders()

        self.assertEqual(result["emails_sent"], 1)
        self.assertEqual(result["alerts_generated"], 0)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Rapport intermédiaire", email.subject)

    @override_settings(REPORTS_DIGEST_RECIPIENTS=["manager@example.com"])
    def test_weekly_campaign_digest_exports_csv(self) -> None:
        result = weekly_campaign_digest()

        self.assertEqual(result["emails_sent"], 1)
        self.assertEqual(result["rows_in_report"], 1)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.attachments[0][0], "digest_affectations.csv")
        self.assertIn("Campagne Printemps", email.attachments[0][1])
