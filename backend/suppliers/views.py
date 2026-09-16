from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from businesses.models import Business

from .models import Supplier
from .serializers import SupplierSerializer
from .services import SupplierService


class BusinessAccessMixin:
    permission_classes = [IsAuthenticated]

    def get_business(self):
        return get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )


class SupplierListCreateView(
    BusinessAccessMixin,
    generics.ListCreateAPIView,
):
    serializer_class = SupplierSerializer

    def get_queryset(self):
        business = self.get_business()

        return Supplier.objects.filter(
            business=business,
        )

    def create(self, request, *args, **kwargs):
        business = self.get_business()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            supplier = SupplierService.create_supplier(
                business=business,
                validated_data=serializer.validated_data,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = self.get_serializer(supplier)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class SupplierDetailView(
    BusinessAccessMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    serializer_class = SupplierSerializer

    def get_queryset(self):
        business = self.get_business()

        return Supplier.objects.filter(
            business=business,
        )

    def perform_update(self, serializer):
        try:
            SupplierService.update_supplier(
                supplier=self.get_object(),
                validated_data=serializer.validated_data,
            )
        except ValueError as error:
            raise ValidationError(
                {"detail": str(error)}
            )
