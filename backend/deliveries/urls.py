from django.urls import path

from .views import (
    AssignDeliveryView,
    CancelDeliveryView,
    CompleteDeliveryView,
    DeliveryDetailView,
    DeliveryListCreateView,
    StartDeliveryView,
)


urlpatterns = [
    path(
        "businesses/<int:business_id>/deliveries/",
        DeliveryListCreateView.as_view(),
        name="delivery-list-create",
    ),

    path(
        "businesses/<int:business_id>/deliveries/<int:pk>/",
        DeliveryDetailView.as_view(),
        name="delivery-detail",
    ),

    path(
        "businesses/<int:business_id>/deliveries/<int:pk>/assign/",
        AssignDeliveryView.as_view(),
        name="delivery-assign",
    ),

    path(
        "businesses/<int:business_id>/deliveries/<int:pk>/start/",
        StartDeliveryView.as_view(),
        name="delivery-start",
    ),

    path(
        "businesses/<int:business_id>/deliveries/<int:pk>/complete/",
        CompleteDeliveryView.as_view(),
        name="delivery-complete",
    ),

    path(
        "businesses/<int:business_id>/deliveries/<int:pk>/cancel/",
        CancelDeliveryView.as_view(),
        name="delivery-cancel",
    ),
]
