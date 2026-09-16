from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from businesses.models import Business

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import ProductService


class BusinessAccessMixin:
    permission_classes = [IsAuthenticated]

    def get_business(self):
        business_id = self.kwargs["business_id"]

        return get_object_or_404(
            Business,
            id=business_id,
            memberships__user=self.request.user,
            memberships__is_active=True,
        )


class CategoryListCreateView(BusinessAccessMixin, generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        business = self.get_business()

        return Category.objects.filter(
            business=business,
        )

    def perform_create(self, serializer):
        business = self.get_business()

        self.created_category = ProductService.create_category(
            business=business,
            validated_data=serializer.validated_data,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = self.get_serializer(
            self.created_category,
        )

        return Response(
            response_serializer.data,
            status=201,
        )


class CategoryDetailView(
    BusinessAccessMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    serializer_class = CategorySerializer

    def get_queryset(self):
        business = self.get_business()

        return Category.objects.filter(
            business=business,
        )

    def perform_update(self, serializer):
        self.updated_category = ProductService.update_category(
            category=self.get_object(),
            validated_data=serializer.validated_data,
        )


class ProductListCreateView(BusinessAccessMixin, generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        business = self.get_business()

        return Product.objects.filter(
            business=business,
        ).select_related("category")

    def perform_create(self, serializer):
        business = self.get_business()

        try:
            self.created_product = ProductService.create_product(
                business=business,
                validated_data=serializer.validated_data,
            )
        except ValueError as error:
            from rest_framework.exceptions import ValidationError

            raise ValidationError(
                {"detail": str(error)}
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = self.get_serializer(
            self.created_product,
        )

        return Response(
            response_serializer.data,
            status=201,
        )


class ProductDetailView(
    BusinessAccessMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    serializer_class = ProductSerializer

    def get_queryset(self):
        business = self.get_business()

        return Product.objects.filter(
            business=business,
        ).select_related("category")

    def perform_update(self, serializer):
        from rest_framework.exceptions import ValidationError

        try:
            self.updated_product = ProductService.update_product(
                product=self.get_object(),
                validated_data=serializer.validated_data,
            )
        except ValueError as error:
            raise ValidationError(
                {"detail": str(error)}
            )
