from decimal import Decimal

from django.db import transaction

from .models import Purchase, StockMovement


class PurchaseService:
    """
    Handles purchase-related business operations.

    Stock changes happen here rather than inside views or serializers.
    """

    @staticmethod
    @transaction.atomic
    def complete_purchase(purchase_id, user):
        """
        Complete a purchase and update product stock atomically.

        Args:
            purchase_id: ID of the purchase to complete.
            user: User performing the operation.

        Returns:
            The completed Purchase instance.

        Raises:
            Purchase.DoesNotExist:
                If the purchase does not exist.

            ValueError:
                If the purchase cannot be completed.
        """

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
            purchase.items.select_related("product").all()
        )

        if not items:
            raise ValueError(
                "A purchase must contain at least one item."
            )

        total_amount = Decimal("0.00")

        for item in items:
            product = (
                item.product.__class__.objects
                .select_for_update()
                .get(id=item.product.id)
            )

            if product.business_id != purchase.business_id:
                raise ValueError(
                    "Purchase item does not belong "
                    "to the purchase business."
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
