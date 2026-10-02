from django.urls import path

from .views import (
    MpesaCallbackView,
    PlanListView,
)

urlpatterns = [
    path(
        "plans/",
        PlanListView.as_view(),
        name="billing-plans",
    ),
    path(
        "mpesa/callback/",
        MpesaCallbackView.as_view(),
        name="mpesa-callback",
    ),
]
