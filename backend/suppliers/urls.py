from django.urls import path

from .views import (
    SupplierDetailView,
    SupplierListCreateView,
)

urlpatterns = [
    path(
        "businesses/<int:business_id>/suppliers/",
        SupplierListCreateView.as_view(),
        name="supplier-list-create",
    ),
    path(
        "businesses/<int:business_id>/suppliers/<int:pk>/",
        SupplierDetailView.as_view(),
        name="supplier-detail",
    ),
]
