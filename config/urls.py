from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

admin.site.index_title = "Tableau de bord"
admin.site.site_title = "Internship MGMT"
admin.site.site_header = "Internship Management"
admin.site.index_template = "admin/index.html"

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

