from django.urls import path

from .views import EntrepriseListView

app_name = "entreprises"

urlpatterns = [
    path("", EntrepriseListView.as_view(), name="list"),
]

