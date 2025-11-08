from django.apps import AppConfig


class EvaluationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "evaluations"
    verbose_name = "Évaluations"

    def ready(self) -> None:
        from . import signals  # noqa: F401

