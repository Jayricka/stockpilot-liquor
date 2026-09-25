from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # Django admin
    path(
        "admin/",
        admin.site.urls,
    ),

    # Authentication
    path(
        "api/auth/",
        include("accounts.urls"),
    ),
    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Business management
    path(
        "api/businesses/",
        include("businesses.urls"),
    ),

    # Products and categories
    path(
        "api/",
        include("products.urls"),
    ),

    # Suppliers
    path(
        "api/",
        include("suppliers.urls"),
    ),

    # Purchases and inventory
    path(
        "api/",
        include("inventory.urls"),
    ),

    # Sales
    path(
        "api/",
        include("sales.urls"),
    ),

    # Deliveries
    path(
        "api/",
        include("deliveries.urls"),
    ),

    # Reports and dashboard
    path(
        "api/",
        include("reports.urls"),
    ),

    # Public interactive demo
    path(
        "api/demo/",
        include("demo.urls"),
    ),
    path(
    "api/billing/",
    include("billing.urls"),
    ),
]
