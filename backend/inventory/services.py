from decimal import Decimal

from django.db import transaction

from products.models import Product

from .models import Purchase, PurchaseItem, StockMovement


class PurchaseService:

    @staticmethod
    @transaction.atomic
    def create_purchase(
        business,
        user,
        validated_data,
        items_data,
    ):
        supplier = validated_data["supplier"]

        if supplier.business_id != business.id:
            raise ValueError(
                "Supplier does not belong to this business."
            )

        purchase = Purchase.objects.create(
            business=business,
            created_by=user,
            **validated_data,
        )

        for item_data in items_data:
            product = item_data["product"]

            if product.business_id != business.id:
                raise ValueError(
                    "Product does not belong to this business."
                )

            PurchaseItem.objects.create(
                purchase=purchase,
                **item_data,
            )

        purchase.update_total()

        return purchase

    @staticmethod
    @transaction.atomic
    def complete_purchase(purchase_id, user):
        purchase = (
            Purchase.objects
            .select_for_update()
            .select_related("business")
            .get(id=purchase_id)
        )

        if purchase.status == Purchase.Status.COMPLETED:
            raise ValueError(
                "This purchase has already been completed."
            )

        if purchase.status == Purchase.Status.CANCELLED:
            raise ValueError(
                "A cancelled purchase cannot be completed."
            )

        items = list(
            purchase.items
            .select_related("product")
            .all()
        )

        if not items:
            raise ValueError(
                "A purchase must contain at least one item."
            )

        total_amount = Decimal("0.00")

        for item in items:
            product = (
                Product.objects
                .select_for_update()
                .get(id=item.product_id)
            )

            if product.business_id != purchase.business_id:
                raise ValueError(
                    "Purchase item does not belong to the purchase business."
                )

            product.increase_stock(item.quantity)

            StockMovement.objects.create(
                business=purchase.business,
                product=product,
                performed_by=user,
                movement_type=StockMovement.MovementType.PURCHASE,
                quantity=item.quantity,
                balance_after=product.stock_quantity,
                reference_id=purchase.id,
                notes=(
                    f"Stock received from purchase "
                    f"{purchase.reference_number}"
                ),
            )

            total_amount += item.line_total

        purchase.total_amount = total_amount
        purchase.status = Purchase.Status.COMPLETED

        purchase.save(
            update_fields=[
                "total_amount",
                "status",
                "updated_at",
            ]
        )

        return purchase

    @staticmethod
    @transaction.atomic
    def cancel_purchase(purchase_id):
        purchase = Purchase.objects.select_for_update().get(
            id=purchase_id
        )

        if purchase.status == Purchase.Status.COMPLETED:
            raise ValueError(
                "A completed purchase cannot be cancelled."
            )

        if purchase.status == Purchase.Status.CANCELLED:
            raise ValueError(
                "This purchase is already cancelled."
            )

        purchase.status = Purchase.Status.CANCELLED

        purchase.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return purchase
