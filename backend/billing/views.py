from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from businesses.models import Business

from .models import (
    Payment,
    Plan,
    PlanEntitlement,
    Subscription,
)
from .serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
    PlanEntitlementSerializer,
    PlanSerializer,
    SubscriptionSerializer,
)
from .services.mpesa import MpesaGatewayError
from .services.mpesa_callbacks import MpesaCallbackService
from .services.payments import PaymentService


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


class BusinessPaymentListCreateView(
    generics.ListCreateAPIView,
):
    permission_classes = [IsAuthenticated]

    def get_business(self):
        return get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PaymentCreateSerializer

        return PaymentSerializer

    def get_queryset(self):
        business = self.get_business()

        return Payment.objects.filter(
            subscription__business=business,
        ).select_related(
            "subscription",
        )

    def create(self, request, *args, **kwargs):
        business = self.get_business()

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        subscription = get_object_or_404(
            Subscription,
            business=business,
        )

        allowed_statuses = {
            Subscription.Status.TRIALING,
            Subscription.Status.ACTIVE,
            Subscription.Status.PAST_DUE,
        }

        if subscription.status not in allowed_statuses:
            return Response(
                {
                    "detail": (
                        "Payments cannot be created for "
                        "this subscription."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = PaymentService.create_payment(
            subscription=subscription,
            amount=serializer.validated_data["amount"],
            phone_number=serializer.validated_data[
                "phone_number"
            ],
            currency=subscription.plan.currency,
        )

        try:
            payment = PaymentService.initiate_mpesa_payment(
                payment=payment,
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except MpesaGatewayError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        response_serializer = PaymentSerializer(
            payment
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class BusinessPaymentDetailView(
    generics.RetrieveAPIView,
):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        business = get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )

        return get_object_or_404(
            Payment.objects.select_related(
                "subscription",
            ),
            id=self.kwargs["payment_id"],
            subscription__business=business,
        )


class MpesaCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            MpesaCallbackService.process_callback(
                request.data
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"ResultCode": 0},
            status=status.HTTP_200_OK,
        )
