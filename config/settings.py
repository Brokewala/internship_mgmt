from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import environ

from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
env.read_env(BASE_DIR / ".env")

SECRET_KEY = 'django-insecure-)9jijekovj+6si)t^65&vr1543!(v!72@*kscxvs6v0sx#8lz^'
DEBUG = env.bool("DEBUG", default=False)


def csv_env(name: str, default: Iterable[str] | None = None) -> list[str]:
    """Parse a comma separated environment variable into a list of values."""

    raw_value = env.str(name, default=None)
    if raw_value is None or raw_value == "":
        return list(default or [])

    return [item.strip() for item in raw_value.split(",") if item.strip()]


ALLOWED_HOSTS = csv_env("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = csv_env("CSRF_TRUSTED_ORIGINS", default=[])

if DEBUG:
    for host in ["localhost", "127.0.0.1", "[::1]"]:
        if host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host)

    for origin in [
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "https://localhost",
        "https://127.0.0.1",
    ]:
        if origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(origin)

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_celery_beat",
    "django_celery_results",
    "rest_framework",
    "django_filters",
    "drf_yasg",
    "import_export",
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    "entreprises.apps.EntreprisesConfig",
    "offres.apps.OffresConfig",
    "candidatures.apps.CandidaturesConfig",
    "affectations.apps.AffectationsConfig",
    "suivis.apps.SuivisConfig",
    "evaluations.apps.EvaluationsConfig",
    "reporting.apps.ReportingConfig",

]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [
                "core.templatetags.compat_filters",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "dbcaros",
        "USER": "dbcaros_user",
        "PASSWORD": "SkU4Z6JCjFBKwcZYbpxOxoSCLTauCj9q",
        "HOST": "dpg-d4boi79r0fns73aoorr0-a.oregon-postgres.render.com",
        "PORT": "5432",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "admin:login"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL", default="noreply@internship-mgmt.local"
)
REPORTS_DIGEST_RECIPIENTS = env.list("REPORTS_DIGEST_RECIPIENTS", default=[])

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {
    "daily_deadline_reminders": {
        "task": "core.tasks.daily_deadline_reminders",
        "schedule": crontab(hour=8, minute=0),
    },
    "weekly_campaign_digest": {
        "task": "core.tasks.weekly_campaign_digest",
        "schedule": crontab(hour=9, minute=0, day_of_week="monday"),
    },
}

IMPORT_EXPORT_USE_TRANSACTIONS = True

JAZZMIN_SETTINGS = {
    "site_title": "Internship MGMT",
    "site_header": "Internship Management",
    "site_brand": "Internship MGMT",
    "site_logo": "images/logo.svg",
    "site_logo_classes": "img-fluid",
    "welcome_sign": "Bienvenue sur votre tableau de bord stages",
    "copyright": "Internship Management",
    "show_ui_builder": False,
    "related_modal_active": True,
    "topmenu_links": [
        {"name": "Accueil", "url": "core:home", "permissions": ["auth.view_user"]},
        {"app": "accounts"},
        {"app": "entreprises"},
        {"app": "offres"},
    ],
    "usermenu_links": [{"name": "Profil", "url": "accounts:profile"}],
    "custom_css": "css/admin_custom.css",
    "hide_apps": ["django_celery_results"],
    "hide_models": [],
    "order_with_respect_to": [
        "accounts",
        "entreprises",
        "offres",
        "candidatures",
        "affectations",
        "suivis",
        "evaluations",
        "reporting",
    ],
    "footer_links": [
        {
            "name": "Documentation",
            "url": "https://intranet.example.com/docs",
            "new_tab": True,
        },
        {
            "name": "Support IT",
            "url": "mailto:support@example.com",
        },
        {
            "name": "Politique de confidentialité",
            "url": "https://intranet.example.com/politique-confidentialite",
            "new_tab": True,
        },
    ],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "cyborg",
    "body_bg": "#f3f4f6",
    "brand_colour": "#1f2937",
    "link_colour": "#2563eb",
    "navbar": "navbar-dark bg-dark",
    "sidebar": "sidebar-dark-primary",
    "button_classes": {
        "primary": "btn btn-primary",
        "secondary": "btn btn-outline-secondary",
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"
USE_X_FORWARDED_HOST = True

