from rest_framework import serializers

from .models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "unit_cost",
            "line_total",
            "line_cost",
            "line_profit",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "unit_price",
            "unit_cost",
            "line_total",
            "line_cost",
            "line_profit",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(
        many=True,
        write_only=True,
    )

    payment_method_display = serializers.CharField(
        source="get_payment_method_display",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.full_name",
        read_only=True,
    )

    class Meta:
        model = Sale
        fields = [
            "id",
            "invoice_number",
            "created_by_name",
            "subtotal",
            "discount_amount",
            "total_amount",
            "total_cost",
            "gross_profit",
            "payment_method",
            "payment_method_display",
            "status",
            "status_display",
            "sale_date",
            "notes",
            "items",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_by_name",
            "subtotal",
            "total_amount",
            "total_cost",
            "gross_profit",
            "status",
            "payment_method_display",
            "status_display",
            "created_at",
        ]

    def validate_invoice_number(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Invoice number is required."
            )

        business = self.context.get("business")

        if business:
            exists = Sale.objects.filter(
                business=business,
                invoice_number=value,
            ).exists()

            if exists:
                raise serializers.ValidationError(
                    "A sale with this invoice number already exists "
                    "in this business."
                )

        return value

    def validate_discount_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Discount cannot be negative."
            )
        return value

    def validate_payment_method(self, value):
        valid_methods = {
            choice[0]
            for choice in Sale.PaymentMethod.choices
        }

        if value not in valid_methods:
            raise serializers.ValidationError(
                "Invalid payment method."
            )

        return value

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError(
                "A sale must contain at least one item."
            )

        business = self.context.get("business")

        if business:
            for item in items:
                product = item["product"]

                if product.business_id != business.id:
                    raise serializers.ValidationError(
                        "Product does not belong to this business."
                    )

        return items
