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
        category = validated_data.get("category")

        if category.business_id != business.id:
            raise ValueError(
                "Category does not belong to this business."
            )

        return Product.objects.create(
            business=business,
            **validated_data,
        )

    @staticmethod
    @transaction.atomic
    def update_product(product, validated_data):
        category = validated_data.get(
            "category",
            product.category,
        )

        if category.business_id != product.business_id:
            raise ValueError(
                "Category does not belong to this business."
            )

        for field, value in validated_data.items():
            setattr(product, field, value)

        product.save()

        return product
