from __future__ import annotations

from django.conf import settings
from django.core.mail import EmailMessage, send_mail

from affectations.models import Affectation
from suivis.models import Livrable


def _format_student_name(user) -> str:
    full_name = user.get_full_name()
    return full_name or user.get_username()


def send_deadline_email(livrable: Livrable) -> int:
    student = livrable.affectation.student
    recipient = student.email
    if not recipient:
        return 0

    subject = f"Rappel : livrable '{livrable.title}' à rendre le {livrable.due_date:%d/%m/%Y}"
    greeting = _format_student_name(student)
    message = (
        f"Bonjour {greeting},\n\n"
        f"Le livrable « {livrable.title} » doit être remis pour le {livrable.due_date:%d/%m/%Y}.\n"
        "Merci de vous assurer que le document est soumis dans la plateforme avant cette date.\n\n"
        "Ceci est un rappel automatique."
    )

    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])


def send_assignment_email(affectation: Affectation) -> int:
    student = affectation.student
    recipient = student.email
    if not recipient:
        return 0

    subject = f"Confirmation d'affectation - {affectation.entreprise.name}"
    greeting = _format_student_name(student)
    body = (
        f"Bonjour {greeting},\n\n"
        f"Votre stage chez {affectation.entreprise.name} est confirmé.\n"
        f"Période : du {affectation.start_date:%d/%m/%Y} au {affectation.end_date:%d/%m/%Y}.\n"
        "Nous vous souhaitons une excellente expérience professionnelle.\n\n"
        "L'équipe pédagogique"
    )

    email = EmailMessage(subject=subject, body=body, from_email=settings.DEFAULT_FROM_EMAIL, to=[recipient])
    return email.send(fail_silently=False)
