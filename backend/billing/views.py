from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from businesses.models import Business

from .models import (
    Payment,
    Plan,
    PlanEntitlement,
    Subscription,
)
from .serializers import (
    PaymentSerializer,
    PlanEntitlementSerializer,
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


class BusinessSubscriptionView(
    generics.RetrieveAPIView,
):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        business = get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )

        return get_object_or_404(
            Subscription.objects.select_related(
                "plan",
                "business",
            ),
            business=business,
        )


class BusinessEntitlementListView(
    generics.ListAPIView,
):
    serializer_class = PlanEntitlementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business = get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )

        return PlanEntitlement.objects.filter(
            plan__subscriptions__business=business,
        ).select_related("plan")


class BusinessPaymentListView(
    generics.ListAPIView,
):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business = get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )

        return Payment.objects.filter(
            subscription__business=business,
        ).select_related(
            "subscription",
        )
