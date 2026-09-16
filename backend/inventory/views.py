from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from businesses.models import Business

from .models import Purchase
from .serializers import PurchaseSerializer
from .services import PurchaseService


class BusinessAccessMixin:
    permission_classes = [IsAuthenticated]

    def get_business(self):
        return get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )


class PurchaseListCreateView(
    BusinessAccessMixin,
    generics.ListCreateAPIView,
):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        business = self.get_business()

        queryset = (
            Purchase.objects
            .filter(business=business)
            .select_related(
                "supplier",
                "created_by",
            )
            .prefetch_related(
                "items__product",
            )
        )

        purchase_status = self.request.query_params.get("status")

        if purchase_status:
            queryset = queryset.filter(
                status=purchase_status,
            )

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["business"] = self.get_business()
        return context

    def create(self, request, *args, **kwargs):
        business = self.get_business()

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        validated_data = serializer.validated_data

        items_data = validated_data.pop(
            "items",
        )

        try:
            purchase = PurchaseService.create_purchase(
                business=business,
                user=request.user,
                validated_data=validated_data,
                items_data=items_data,
            )

        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = self.get_serializer(
            purchase,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PurchaseDetailView(
    BusinessAccessMixin,
    generics.RetrieveAPIView,
):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        business = self.get_business()

        return (
            Purchase.objects
            .filter(business=business)
            .select_related(
                "supplier",
                "created_by",
            )
            .prefetch_related(
                "items__product",
            )
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["business"] = self.get_business()
        return context


class CompletePurchaseView(
    BusinessAccessMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def post(self, request, business_id, pk):
        business = self.get_business()

        purchase = get_object_or_404(
            Purchase,
            id=pk,
            business=business,
        )

        try:
            purchase = PurchaseService.complete_purchase(
                purchase_id=purchase.id,
                user=request.user,
            )

        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            purchase,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CancelPurchaseView(
    BusinessAccessMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def post(self, request, business_id, pk):
        business = self.get_business()

        purchase = get_object_or_404(
            Purchase,
            id=pk,
            business=business,
        )

        try:
            purchase = PurchaseService.cancel_purchase(
                purchase_id=purchase.id,
            )

        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            purchase,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
