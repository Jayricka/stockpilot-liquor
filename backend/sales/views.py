from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from billing.permissions import HasOperationalAccess
from businesses.models import Business

from .models import Sale
from .serializers import SaleSerializer
from .services import SaleService


class BusinessAccessMixin:
    permission_classes = [
        IsAuthenticated,
        HasOperationalAccess,
    ]

    def get_business(self):
        return get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )


class SaleListCreateView(
    BusinessAccessMixin,
    generics.ListCreateAPIView,
):
    serializer_class = SaleSerializer

    def get_queryset(self):
        business = self.get_business()

        queryset = (
            Sale.objects
            .filter(business=business)
            .select_related("created_by")
            .prefetch_related("items__product")
        )

        sale_status = self.request.query_params.get("status")

        if sale_status:
            queryset = queryset.filter(
                status=sale_status
            )

        payment_method = self.request.query_params.get(
            "payment_method"
        )

        if payment_method:
            queryset = queryset.filter(
                payment_method=payment_method
            )

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["business"] = self.get_business()
        return context

    def create(self, request, *args, **kwargs):
        business = self.get_business()

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = serializer.validated_data
        items_data = validated_data.pop("items")

        try:
            sale = SaleService.create_sale(
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

        response_serializer = self.get_serializer(sale)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class SaleDetailView(
    BusinessAccessMixin,
    generics.RetrieveAPIView,
):
    serializer_class = SaleSerializer

    def get_queryset(self):
        business = self.get_business()

        return (
            Sale.objects
            .filter(business=business)
            .select_related("created_by")
            .prefetch_related("items__product")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["business"] = self.get_business()
        return context


class CompleteSaleView(
    BusinessAccessMixin,
    generics.GenericAPIView,
):
    serializer_class = SaleSerializer

    def post(self, request, business_id, pk):
        business = self.get_business()

        sale = get_object_or_404(
            Sale,
            id=pk,
            business=business,
        )

        try:
            sale = SaleService.complete_sale(
                sale_id=sale.id,
                user=request.user,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(sale)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CancelSaleView(
    BusinessAccessMixin,
    generics.GenericAPIView,
):
    serializer_class = SaleSerializer

    def post(self, request, business_id, pk):
        business = self.get_business()

        sale = get_object_or_404(
            Sale,
            id=pk,
            business=business,
        )

        try:
            sale = SaleService.cancel_sale(
                sale_id=sale.id,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(sale)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
