from django.urls import path

from .views import SuiviListView

app_name = "suivis"

urlpatterns = [
    path("", SuiviListView.as_view(), name="list"),
]

