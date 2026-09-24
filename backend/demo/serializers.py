from decimal import Decimal

from rest_framework import serializers

from products.models import Product


class DemoProductSerializer(
    serializers.ModelSerializer
):
    is_low_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id",
            "brand",
            "name",
            "unit",
            "buying_price",
            "selling_price",
            "stock_quantity",
            "reorder_level",
            "is_low_stock",
        ]


class DemoActionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    quantity = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
