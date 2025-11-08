from django.urls import path

from .views import OffreListView

app_name = "offres"

urlpatterns = [
    path("", OffreListView.as_view(), name="list"),
]

