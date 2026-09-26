from django.urls import path

from .onboarding_views import BusinessOnboardingView
from .views import (
    BusinessDetailView,
    BusinessListCreateView,
    BusinessMemberCreateView,
    BusinessMemberDeactivateView,
    BusinessMemberListView,
    BusinessMemberRoleUpdateView,
)


urlpatterns = [
    path(
        "",
        BusinessListCreateView.as_view(),
        name="business-list-create",
    ),
    path(
        "onboard/",
        BusinessOnboardingView.as_view(),
        name="business-onboard",
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
        "<int:business_id>/members/add/",
        BusinessMemberCreateView.as_view(),
        name="business-member-add",
    ),
    path(
        "<int:business_id>/members/<int:user_id>/role/",
        BusinessMemberRoleUpdateView.as_view(),
        name="business-member-role",
    ),
    path(
        "<int:business_id>/members/<int:user_id>/",
        BusinessMemberDeactivateView.as_view(),
        name="business-member-deactivate",
    ),
]
