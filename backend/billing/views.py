from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from businesses.models import BusinessMembership

from .models import Plan, Subscription
from .serializers import (
    PlanSerializer,
    SubscriptionSerializer,
)


class PlanListView(generics.ListAPIView):
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Plan.objects.filter(
            is_active=True,
        )


class CurrentSubscriptionView(
    generics.RetrieveAPIView,
):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        membership = (
            BusinessMembership.objects
            .filter(
                user=self.request.user,
                is_active=True,
            )
            .select_related("business")
            .first()
        )

        if not membership:
            raise NotFound(
                "You do not belong to an active business."
            )

        try:
            return Subscription.objects.select_related(
                "plan",
                "business",
            ).get(
                business=membership.business,
            )
        except Subscription.DoesNotExist:
            raise NotFound(
                "This business does not have a subscription."
            )
