from django.urls import path

from .views import (
    CancelPurchaseView,
    CompletePurchaseView,
    PurchaseDetailView,
    PurchaseListCreateView,
)


urlpatterns = [
    path(
        "businesses/<int:business_id>/purchases/",
        PurchaseListCreateView.as_view(),
        name="purchase-list-create",
    ),
    path(
        "businesses/<int:business_id>/purchases/<int:pk>/",
        PurchaseDetailView.as_view(),
        name="purchase-detail",
    ),
    path(
        "businesses/<int:business_id>/purchases/<int:pk>/complete/",
        CompletePurchaseView.as_view(),
        name="purchase-complete",
    ),
    path(
        "businesses/<int:business_id>/purchases/<int:pk>/cancel/",
        CancelPurchaseView.as_view(),
        name="purchase-cancel",
    ),
]
