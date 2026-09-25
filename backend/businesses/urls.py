from django.urls import path
from .onboarding_views import BusinessOnboardingView

from .views import (
    BusinessDetailView,
    BusinessListCreateView,
    BusinessMemberListView,
)

urlpatterns = [
    path(
        "",
        BusinessListCreateView.as_view(),
        name="business-list-create",
    ),
    path(
        "<int:business_id>/",
        BusinessDetailView.as_view(),
        name="business-detail",
    ),
    path(
        "<int:business_id>/members/",
        BusinessMemberListView.as_view(),
        name="business-member-list",
    ),
    path(
    "onboard/",
    BusinessOnboardingView.as_view(),
    name="business-onboard",
),
]
