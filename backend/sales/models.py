from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from businesses.models import Business
from products.models import Product


class Sale(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        MPESA = "MPESA", "M-Pesa"
        CARD = "CARD", "Card"
        CREDIT = "CREDIT", "Credit"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="sales",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_sales",
    )

    invoice_number = models.CharField(
        max_length=100,
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    total_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    gross_profit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    sale_date = models.DateField()

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "-sale_date",
            "-created_at",
        ]
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "business",
                    "invoice_number",
                ],
                name="unique_invoice_per_business",
            )
        ]

    def __str__(self):
        return self.invoice_number

    def calculate_totals(self):
        subtotal = sum(
            (
                item.line_total
                for item in self.items.all()
            ),
            Decimal("0.00"),
        )

        total_cost = sum(
            (
                item.line_cost
                for item in self.items.all()
            ),
            Decimal("0.00"),
        )

        total_amount = subtotal - self.discount_amount
        gross_profit = total_amount - total_cost

        return {
            "subtotal": subtotal,
            "total_cost": total_cost,
            "total_amount": total_amount,
            "gross_profit": gross_profit,
        }


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_items",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )

    # These fields preserve historical sale prices.
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    line_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    line_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    line_profit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    def save(self, *args, **kwargs):
        self.line_total = (
            self.quantity * self.unit_price
        )

        self.line_cost = (
            self.quantity * self.unit_cost
        )

        self.line_profit = (
            self.line_total - self.line_cost
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.product.name} - "
            f"{self.quantity}"
        )
