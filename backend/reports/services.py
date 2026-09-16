from decimal import Decimal

from django.db.models import Count, F, Sum
from django.utils import timezone

from deliveries.models import DeliveryOrder
from inventory.models import Purchase
from products.models import Product
from sales.models import Sale


class DashboardService:

    @staticmethod
    def get_dashboard(business):
        today = timezone.localdate()

        completed_sales = Sale.objects.filter(
            business=business,
            status=Sale.Status.COMPLETED,
        )

        today_sales = completed_sales.filter(
            sale_date=today,
        )

        completed_purchases = Purchase.objects.filter(
            business=business,
            status=Purchase.Status.COMPLETED,
        )

        products = Product.objects.filter(
            business=business,
            is_active=True,
        )

        low_stock_products = products.filter(
            stock_quantity__lte=F("reorder_level"),
        )

        pending_deliveries = DeliveryOrder.objects.filter(
            business=business,
            status__in=[
                DeliveryOrder.Status.PENDING,
                DeliveryOrder.Status.ASSIGNED,
                DeliveryOrder.Status.OUT_FOR_DELIVERY,
            ],
        )

        revenue = today_sales.aggregate(
            total=Sum("total_amount")
        )["total"] or Decimal("0.00")

        gross_profit = today_sales.aggregate(
            total=Sum("gross_profit")
        )["total"] or Decimal("0.00")

        total_stock_value = products.aggregate(
            total=Sum(
                F("stock_quantity") * F("buying_price")
            )
        )["total"] or Decimal("0.00")

        sales_count = today_sales.count()

        total_products = products.count()

        low_stock_count = low_stock_products.count()

        pending_delivery_count = pending_deliveries.count()

        payment_methods = list(
            today_sales
            .values("payment_method")
            .annotate(
                total=Sum("total_amount"),
                count=Count("id"),
            )
            .order_by("-total")
        )

        top_products = list(
            today_sales
            .values(
                "items__product_id",
                "items__product__name",
            )
            .annotate(
                quantity=Sum("items__quantity"),
                revenue=Sum("items__line_total"),
            )
            .order_by("-quantity")[:5]
        )

        recent_sales = list(
            completed_sales
            .select_related("created_by")
            .order_by("-created_at")[:5]
            .values(
                "id",
                "invoice_number",
                "total_amount",
                "gross_profit",
                "payment_method",
                "sale_date",
            )
        )

        recent_purchases = list(
            completed_purchases
            .select_related("supplier")
            .order_by("-created_at")[:5]
            .values(
                "id",
                "reference_number",
                "supplier__name",
                "total_amount",
                "purchase_date",
            )
        )

        low_stock = list(
            low_stock_products
            .select_related("category")
            .order_by("stock_quantity")[:10]
            .values(
                "id",
                "name",
                "sku",
                "stock_quantity",
                "reorder_level",
                "unit",
                "category__name",
            )
        )

        return {
            "date": today,
            "summary": {
                "today_sales_count": sales_count,
                "today_revenue": revenue,
                "today_gross_profit": gross_profit,
                "total_products": total_products,
                "low_stock_count": low_stock_count,
                "total_stock_value": total_stock_value,
                "pending_delivery_count": pending_delivery_count,
            },
            "sales_by_payment_method": payment_methods,
            "top_products": top_products,
            "low_stock_products": low_stock,
            "recent_sales": recent_sales,
            "recent_purchases": recent_purchases,
        }
