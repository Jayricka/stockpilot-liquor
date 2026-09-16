from rest_framework import serializers

from .models import Purchase, PurchaseItem


class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = PurchaseItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_cost",
            "line_total",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "line_total",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )

        return value

    def validate_unit_cost(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Unit cost cannot be negative."
            )

        return value


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(
        many=True,
        write_only=True,
    )

    supplier_name = serializers.CharField(
        source="supplier.name",
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.full_name",
        read_only=True,
    )

    class Meta:
        model = Purchase
        fields = [
            "id",
            "supplier",
            "supplier_name",
            "created_by_name",
            "reference_number",
            "total_amount",
            "status",
            "purchase_date",
            "notes",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "supplier_name",
            "created_by_name",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_reference_number(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Reference number is required."
            )

        business = self.context.get("business")

        if business:
            existing_purchase = Purchase.objects.filter(
                business=business,
                reference_number=value,
            ).first()

            if existing_purchase:
                raise serializers.ValidationError(
                    "A purchase with this reference number "
                    "already exists in this business."
                )

        return value

    def validate_supplier(self, supplier):
        business = self.context.get("business")

        if business and supplier.business_id != business.id:
            raise serializers.ValidationError(
                "Supplier does not belong to this business."
            )

        return supplier

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError(
                "A purchase must contain at least one item."
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
