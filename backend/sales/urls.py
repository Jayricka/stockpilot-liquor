from django.urls import path

from .views import (
    CancelSaleView,
    CompleteSaleView,
    SaleDetailView,
    SaleListCreateView,
)


urlpatterns = [
    path(
        "businesses/<int:business_id>/sales/",
        SaleListCreateView.as_view(),
        name="sale-list-create",
    ),
    path(
        "businesses/<int:business_id>/sales/<int:pk>/",
        SaleDetailView.as_view(),
        name="sale-detail",
    ),
    path(
        "businesses/<int:business_id>/sales/<int:pk>/complete/",
        CompleteSaleView.as_view(),
        name="sale-complete",
    ),
    path(
        "businesses/<int:business_id>/sales/<int:pk>/cancel/",
        CancelSaleView.as_view(),
        name="sale-cancel",
    ),
]
