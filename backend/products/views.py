from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from billing.permissions import HasOperationalAccess
from businesses.models import BusinessMembership

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import ProductService


class BusinessScopedMixin:

    def get_business(self):
        business_id = self.kwargs["business_id"]

        membership = (
            BusinessMembership.objects
            .filter(
                user=self.request.user,
                business_id=business_id,
                is_active=True,
            )
            .select_related("business")
            .first()
        )

        if membership is None:
            raise NotFound(
                "You do not have access to this business."
            )

        return membership.business


class CategoryListCreateView(
    BusinessScopedMixin,
    generics.ListCreateAPIView,
):
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticated,
        HasOperationalAccess,
    ]

    def get_queryset(self):
        business = self.get_business()

        return (
            Category.objects
            .filter(business=business)
            .order_by("group", "name")
        )

    def perform_create(self, serializer):
        business = self.get_business()

        try:
            category = ProductService.create_category(
                business=business,
                validated_data=serializer.validated_data,
            )
        except ValueError as exc:
            raise ValidationError(
                {"detail": str(exc)}
            ) from exc

        serializer.instance = category


class CategoryDetailView(
    BusinessScopedMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticated,
        HasOperationalAccess,
    ]

    def get_queryset(self):
        business = self.get_business()

        return Category.objects.filter(
            business=business
        )

    def perform_update(self, serializer):
        try:
            ProductService.update_category(
                category=self.get_object(),
                validated_data=serializer.validated_data,
            )
        except ValueError as exc:
            raise ValidationError(
                {"detail": str(exc)}
            ) from exc


class ProductListCreateView(
    BusinessScopedMixin,
    generics.ListCreateAPIView,
):
    serializer_class = ProductSerializer
    permission_classes = [
        IsAuthenticated,
        HasOperationalAccess,
    ]

    def get_queryset(self):
        business = self.get_business()

        return (
            Product.objects
            .filter(business=business)
            .select_related("category")
            .order_by("name")
        )

    def perform_create(self, serializer):
        business = self.get_business()

        try:
            product = ProductService.create_product(
                business=business,
                validated_data=serializer.validated_data,
            )
        except ValueError as exc:
            raise ValidationError(
                {"detail": str(exc)}
            ) from exc

        serializer.instance = product


class ProductDetailView(
    BusinessScopedMixin,
    generics.RetrieveUpdateAPIView,
):
    serializer_class = ProductSerializer
    permission_classes = [
        IsAuthenticated,
        HasOperationalAccess,
    ]

    def get_queryset(self):
        business = self.get_business()

        return (
            Product.objects
            .filter(business=business)
            .select_related("category")
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            self.perform_update(serializer)
        except ValueError as exc:
            raise ValidationError(
                {"detail": str(exc)}
            ) from exc

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def perform_update(self, serializer):
        ProductService.update_product(
            product=self.get_object(),
            validated_data=serializer.validated_data,
        )
