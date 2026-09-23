from decimal import Decimal

from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    group_display = serializers.CharField(
        source="get_group_display",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "group",
            "group_display",
            "description",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "group_display",
            "created_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    category_group = serializers.CharField(
        source="category.group",
        read_only=True,
    )

    category_group_display = serializers.CharField(
        source="category.get_group_display",
        read_only=True,
    )

    initial_quantity = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_name",
            "category_group",
            "category_group_display",
            "brand",
            "name",
            "sku",
            "unit",
            "buying_price",
            "selling_price",
            "stock_quantity",
            "initial_quantity",
            "reorder_level",
            "is_active",
            "is_low_stock",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "category_name",
            "category_group",
            "category_group_display",
            "stock_quantity",
            "is_low_stock",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        """
        Validate product-level business rules.

        Handles both:
        - product creation
        - partial/full product updates
        """

        if (
            self.instance is not None
            and "initial_quantity" in attrs
        ):
            raise serializers.ValidationError(
                {
                    "initial_quantity": (
                        "Opening quantity can only be set "
                        "when creating a product."
                    )
                }
            )

        buying_price = attrs.get(
            "buying_price",
            getattr(
                self.instance,
                "buying_price",
                None,
            ),
        )

        selling_price = attrs.get(
            "selling_price",
            getattr(
                self.instance,
                "selling_price",
                None,
            ),
        )

        if (
            buying_price is not None
            and selling_price is not None
            and selling_price < buying_price
        ):
            raise serializers.ValidationError(
                {
                    "selling_price": (
                        "Selling price cannot be lower than "
                        "buying price."
                    )
                }
            )

        return attrs
