from django.urls import path

from .views import (
    CurrentSubscriptionView,
    PlanListView,
)


urlpatterns = [
    path(
        "plans/",
        PlanListView.as_view(),
        name="billing-plans",
    ),
    path(
        "subscription/",
        CurrentSubscriptionView.as_view(),
        name="current-subscription",
    ),
]
