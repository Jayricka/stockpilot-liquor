from django.urls import path

from .views import DashboardView


urlpatterns = [
    path(
        "businesses/<int:business_id>/reports/dashboard/",
        DashboardView.as_view(),
        name="dashboard",
    ),
]
