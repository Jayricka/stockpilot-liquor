from decimal import Decimal

from django.db import transaction

from inventory.models import StockMovement
from products.models import Product

from .models import Sale, SaleItem


class SaleService:

    @staticmethod
    @transaction.atomic
    def create_sale(
        business,
        user,
        validated_data,
        items_data,
    ):
        sale = Sale.objects.create(
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

            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=item_data["quantity"],
            )

        return sale

    @staticmethod
    @transaction.atomic
    def complete_sale(sale_id, user):
        sale = (
            Sale.objects
            .select_for_update()
            .select_related("business")
            .get(id=sale_id)
        )

        if sale.status == Sale.Status.COMPLETED:
            raise ValueError(
                "This sale has already been completed."
            )

        if sale.status == Sale.Status.CANCELLED:
            raise ValueError(
                "A cancelled sale cannot be completed."
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
                Product.objects
                .select_for_update()
                .get(id=item.product_id)
            )

            if product.business_id != sale.business_id:
                raise ValueError(
                    "Sale item does not belong to the sale business."
                )

            if not product.has_sufficient_stock(
                item.quantity
            ):
                raise ValueError(
                    f"Insufficient stock for {product.name}."
                )

            item.unit_price = product.selling_price
            item.unit_cost = product.buying_price

            item.line_total = (
                item.quantity * item.unit_price
            )

            item.line_cost = (
                item.quantity * item.unit_cost
            )

            item.line_profit = (
                item.line_total - item.line_cost
            )

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
                    f"Stock deducted from sale "
                    f"{sale.invoice_number}"
                ),
            )

            subtotal += item.line_total
            total_cost += item.line_cost

        discount = sale.discount_amount or Decimal("0.00")

        total_amount = subtotal - discount

        if total_amount < Decimal("0.00"):
            raise ValueError(
                "Discount cannot exceed the sale subtotal."
            )

        sale.subtotal = subtotal
        sale.total_amount = total_amount
        sale.total_cost = total_cost
        sale.gross_profit = total_amount - total_cost
        sale.status = Sale.Status.COMPLETED

        sale.save(
            update_fields=[
                "subtotal",
                "total_amount",
                "total_cost",
                "gross_profit",
                "status",
            ]
        )

        return sale

    @staticmethod
    @transaction.atomic
    def cancel_sale(sale_id):
        sale = (
            Sale.objects
            .select_for_update()
            .get(id=sale_id)
        )

        if sale.status == Sale.Status.COMPLETED:
            raise ValueError(
                "A completed sale cannot be cancelled."
            )

        if sale.status == Sale.Status.CANCELLED:
            raise ValueError(
                "This sale is already cancelled."
            )

        sale.status = Sale.Status.CANCELLED
        sale.save(
            update_fields=["status"]
        )

        return sale
