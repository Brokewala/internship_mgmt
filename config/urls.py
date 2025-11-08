from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

admin.site.index_title = "Tableau de bord"
admin.site.site_title = "Internship MGMT"
admin.site.site_header = "Internship Management"
admin.site.index_template = "admin/index.html"

schema_view = get_schema_view(
    openapi.Info(
        title="Internship Management API",
        default_version="v1",
        description="API de gestion des stages",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("entreprises/", include("entreprises.urls", namespace="entreprises")),
    path("offres/", include("offres.urls", namespace="offres")),
    path("candidatures/", include("candidatures.urls", namespace="candidatures")),
    path("affectations/", include("affectations.urls", namespace="affectations")),
    path("suivis/", include("suivis.urls", namespace="suivis")),
    path("evaluations/", include("evaluations.urls", namespace="evaluations")),
    path("reporting/", include("reporting.urls", namespace="reporting")),
    path("accounts/profile", RedirectView.as_view(pattern_name="accounts:profile", permanent=False)),
    path("api/v1/", include("api.urls", namespace="api")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/docs/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

