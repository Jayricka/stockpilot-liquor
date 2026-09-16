from rest_framework import serializers

from .models import DeliveryOrder


class DeliveryOrderSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(
        source="sale.invoice_number",
        read_only=True,
    )

    assigned_to_name = serializers.CharField(
        source="assigned_to.full_name",
        read_only=True,
    )

    assigned_to_email = serializers.EmailField(
        source="assigned_to.email",
        read_only=True,
    )

    class Meta:
        model = DeliveryOrder

        fields = [
            "id",
            "sale",
            "invoice_number",
            "customer_name",
            "customer_phone",
            "delivery_address",
            "assigned_to",
            "assigned_to_name",
            "assigned_to_email",
            "delivery_fee",
            "status",
            "notes",
            "assigned_at",
            "delivered_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "invoice_number",
            "assigned_to_name",
            "assigned_to_email",
            "status",
            "assigned_at",
            "delivered_at",
            "created_at",
            "updated_at",
        ]

    def validate_sale(self, sale):
        business = self.context.get("business")

        if business and sale.business_id != business.id:
            raise serializers.ValidationError(
                "Sale does not belong to this business."
            )

        if sale.status != sale.Status.COMPLETED:
            raise serializers.ValidationError(
                "Only completed sales can have delivery orders."
            )

        if DeliveryOrder.objects.filter(
            sale=sale
        ).exists():
            raise serializers.ValidationError(
                "This sale already has a delivery order."
            )

        return sale

    def validate_delivery_fee(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Delivery fee cannot be negative."
            )

        return value
