from django.urls import path

from .views import CandidatureListView

app_name = "candidatures"

urlpatterns = [
    path("", CandidatureListView.as_view(), name="list"),
]

