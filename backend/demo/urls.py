from django.urls import path

from .views import (
    DemoPurchaseView,
    DemoSaleView,
    DemoStartView,
    DemoStateView,
)


urlpatterns = [
    path(
        "start/",
        DemoStartView.as_view(),
        name="demo-start",
    ),
    path(
        "<uuid:token>/",
        DemoStateView.as_view(),
        name="demo-state",
    ),
    path(
        "<uuid:token>/purchase/",
        DemoPurchaseView.as_view(),
        name="demo-purchase",
    ),
    path(
        "<uuid:token>/sale/",
        DemoSaleView.as_view(),
        name="demo-sale",
    ),
]
