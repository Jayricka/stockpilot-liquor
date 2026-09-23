from django.urls import path

from .views import (
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
        "<int:business_id>/members/",
        BusinessMemberListView.as_view(),
        name="business-member-list",
    ),
]
