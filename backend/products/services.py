from django.db import transaction

from .models import Category, Product


class ProductService:

    @staticmethod
    @transaction.atomic
    def create_category(business, validated_data):
        return Category.objects.create(
            business=business,
            **validated_data,
        )

    @staticmethod
    @transaction.atomic
    def update_category(category, validated_data):
        for field, value in validated_data.items():
            setattr(category, field, value)

        category.save()

        return category

    @staticmethod
    @transaction.atomic
    def create_product(business, validated_data):
        data = validated_data.copy()

        category = data.pop("category")

        initial_quantity = data.pop(
            "initial_quantity",
            0,
        )

        if category.business_id != business.id:
            raise ValueError(
                "Category does not belong to this business."
            )

        return Product.objects.create(
            business=business,
            category=category,
            stock_quantity=initial_quantity,
            **data,
        )

    @staticmethod
    @transaction.atomic
    def update_product(product, validated_data):
        data = validated_data.copy()

        if "initial_quantity" in data:
            raise ValueError(
                "Opening quantity cannot be changed "
                "after product creation."
            )

        category = data.pop(
            "category",
            product.category,
        )

        if category.business_id != product.business_id:
            raise ValueError(
                "Category does not belong to this business."
            )

        for field, value in data.items():
            setattr(product, field, value)

        product.category = category
        product.save()

        return product
