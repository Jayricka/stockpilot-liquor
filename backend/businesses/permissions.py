from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from .models import BusinessMembership


class CanManageBusiness(BasePermission):
    message = (
        "Only business owners and managers can update "
        "business information."
    )

    def has_object_permission(
        self,
        request,
        view,
        business,
    ):
        if request.method in SAFE_METHODS:
            return True

        return BusinessMembership.objects.filter(
            user=request.user,
            business=business,
            is_active=True,
            role__in=[
                BusinessMembership.Role.OWNER,
                BusinessMembership.Role.MANAGER,
            ],
        ).exists()


class CanManageMembers(BasePermission):
    message = (
        "Only business owners and managers can "
        "manage business members."
    )

    def has_permission(self, request, view):
        business_id = view.kwargs.get("business_id")

        if not business_id:
            return False

        return BusinessMembership.objects.filter(
            user=request.user,
            business_id=business_id,
            is_active=True,
            role__in=[
                BusinessMembership.Role.OWNER,
                BusinessMembership.Role.MANAGER,
            ],
        ).exists()
