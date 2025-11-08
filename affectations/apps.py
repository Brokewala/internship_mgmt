from django.apps import AppConfig


class AffectationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "affectations"
    verbose_name = "Affectations"

    def ready(self) -> None:
        from . import signals  # noqa: F401

