from django.urls import path

from .views import (
    CategoryDetailView,
    CategoryListCreateView,
    ProductDetailView,
    ProductListCreateView,
)

urlpatterns = [
    path(
        "businesses/<int:business_id>/categories/",
        CategoryListCreateView.as_view(),
        name="category-list-create",
    ),
    path(
        "businesses/<int:business_id>/categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "businesses/<int:business_id>/products/",
        ProductListCreateView.as_view(),
        name="product-list-create",
    ),
    path(
        "businesses/<int:business_id>/products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
]
