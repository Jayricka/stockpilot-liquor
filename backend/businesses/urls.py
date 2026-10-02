from django.urls import path

from billing.views import (
    BusinessEntitlementListView,
    BusinessPaymentDetailView,
    BusinessPaymentListCreateView,
    BusinessSubscriptionView,
)

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
        name="business-members",
    ),
    path(
        "<int:business_id>/subscription/",
        BusinessSubscriptionView.as_view(),
        name="business-subscription",
    ),
    path(
        "<int:business_id>/entitlements/",
        BusinessEntitlementListView.as_view(),
        name="business-entitlements",
    ),
    path(
        "<int:business_id>/payments/",
        BusinessPaymentListCreateView.as_view(),
        name="business-payments",
    ),
    path(
        "<int:business_id>/payments/<int:payment_id>/",
        BusinessPaymentDetailView.as_view(),
        name="business-payment-detail",
    ),
]
