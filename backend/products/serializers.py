from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "sku",
            "unit",
            "buying_price",
            "selling_price",
            "stock_quantity",
            "reorder_level",
            "is_active",
            "is_low_stock",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "stock_quantity",
            "is_low_stock",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        buying_price = attrs.get(
            "buying_price",
            getattr(self.instance, "buying_price", None),
        )

        selling_price = attrs.get(
            "selling_price",
            getattr(self.instance, "selling_price", None),
        )

        if (
            buying_price is not None
            and selling_price is not None
            and selling_price < buying_price
        ):
            raise serializers.ValidationError(
                {
                    "selling_price": (
                        "Selling price cannot be lower than buying price."
                    )
                }
            )

        return attrs
