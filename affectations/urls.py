from django.urls import path

from .views import AffectationListView

app_name = "affectations"

urlpatterns = [
    path("", AffectationListView.as_view(), name="list"),
]

