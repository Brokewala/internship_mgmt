from django.urls import path

from .views import EvaluationListView

app_name = "evaluations"

urlpatterns = [
    path("", EvaluationListView.as_view(), name="list"),
]

