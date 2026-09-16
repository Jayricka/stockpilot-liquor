from django.urls import path

from .views import BusinessListCreateView

urlpatterns = [
    path(
        "",
        BusinessListCreateView.as_view(),
        name="business-list-create",
    ),
]
