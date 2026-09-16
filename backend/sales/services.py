from decimal import Decimal

from django.db import transaction

from inventory.models import StockMovement

from .models import Sale


class SaleService:
    """
    Handles sale-related business operations.

    Stock deduction, financial calculations, and stock
    movement creation happen inside one database transaction.
    """

    @staticmethod
    @transaction.atomic
    def complete_sale(sale_id, user):
        sale = (
            Sale.objects
            .select_for_update()
            .get(id=sale_id)
        )

        if sale.status == Sale.Status.CANCELLED:
            raise ValueError(
                "A cancelled sale cannot be completed."
            )

        if sale.status == Sale.Status.COMPLETED:
            raise ValueError(
                "This sale has already been completed."
            )

        items = list(
            sale.items.select_related("product").all()
        )

        if not items:
            raise ValueError(
                "A sale must contain at least one item."
            )

        subtotal = Decimal("0.00")
        total_cost = Decimal("0.00")

        for item in items:
            product = (
                item.product.__class__.objects
                .select_for_update()
                .get(id=item.product.id)
            )

            if product.business_id != sale.business_id:
                raise ValueError(
                    "Sale item does not belong "
                    "to the sale business."
                )

            if not product.has_sufficient_stock(
                item.quantity
            ):
                raise ValueError(
                    f"Insufficient stock for "
                    f"{product.name}. "
                    f"Available: {product.stock_quantity}, "
                    f"Requested: {item.quantity}."
                )

            # Snapshot current product prices.
            item.unit_price = product.selling_price
            item.unit_cost = product.buying_price
            item.save(
                update_fields=[
                    "unit_price",
                    "unit_cost",
                    "line_total",
                    "line_cost",
                    "line_profit",
                ]
            )

            product.reduce_stock(item.quantity)

            StockMovement.objects.create(
                business=sale.business,
                product=product,
                performed_by=user,
                movement_type=StockMovement.MovementType.SALE,
                quantity=-item.quantity,
                balance_after=product.stock_quantity,
                reference_id=sale.id,
                notes=(
                    f"Stock sold through invoice "
                    f"{sale.invoice_number}"
                ),
            )

            subtotal += item.line_total
            total_cost += item.line_cost

        total_amount = subtotal - sale.discount_amount

        if total_amount < Decimal("0.00"):
            raise ValueError(
                "Discount cannot exceed the sale subtotal."
            )

        sale.subtotal = subtotal
        sale.total_cost = total_cost
        sale.total_amount = total_amount
        sale.gross_profit = total_amount - total_cost
        sale.status = Sale.Status.COMPLETED

        sale.save(
            update_fields=[
                "subtotal",
                "total_cost",
                "total_amount",
                "gross_profit",
                "status",
            ]
        )

        return sale
