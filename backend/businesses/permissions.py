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
