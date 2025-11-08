from django.urls import path

from .views import ReportSnapshotListView

app_name = "reporting"

urlpatterns = [
    path("", ReportSnapshotListView.as_view(), name="list"),
]

