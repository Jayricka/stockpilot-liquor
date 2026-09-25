from rest_framework.permissions import BasePermission

from businesses.models import BusinessMembership

from .models import Subscription
from .services.subscriptions import SubscriptionService


class HasOperationalAccess(BasePermission):
    message = (
        "Your subscription is not active. "
        "Please renew your subscription to continue."
    )

    def has_permission(self, request, view):
        business_id = view.kwargs.get("business_id")

        if not business_id:
            return True

        membership = (
            BusinessMembership.objects
            .filter(
                user=request.user,
                business_id=business_id,
                is_active=True,
            )
            .select_related("business")
            .first()
        )

        if membership is None:
            return True

        try:
            subscription = (
                Subscription.objects
                .select_related("plan")
                .get(
                    business=membership.business,
                )
            )
        except Subscription.DoesNotExist:
            return False

        SubscriptionService.expire_trial(subscription)

        return subscription.status in {
            Subscription.Status.TRIALING,
            Subscription.Status.ACTIVE,
        }
