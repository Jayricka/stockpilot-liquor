from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from businesses.models import Business


class Category(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        constraints = [
            models.UniqueConstraint(
                fields=["business", "name"],
                name="unique_category_per_business",
            )
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    class Unit(models.TextChoices):
        BOTTLE = "BOTTLE", "Bottle"
        LITRE = "LITRE", "Litre"
        CRATE = "CRATE", "Crate"
        PIECE = "PIECE", "Piece"

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="products",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    name = models.CharField(max_length=150)

    sku = models.CharField(
        max_length=50,
        blank=True,
    )

    unit = models.CharField(
        max_length=20,
        choices=Unit.choices,
        default=Unit.BOTTLE,
    )

    buying_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    stock_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    reorder_level = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
        constraints = [
            models.UniqueConstraint(
                fields=["business", "sku"],
                name="unique_sku_per_business",
            )
        ]

    def __str__(self):
        return self.name

    def has_sufficient_stock(self, quantity):
        return self.stock_quantity >= quantity

    def increase_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.stock_quantity += quantity
        self.save(update_fields=["stock_quantity", "updated_at"])

    def reduce_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if not self.has_sufficient_stock(quantity):
            raise ValueError("Insufficient stock.")

        self.stock_quantity -= quantity
        self.save(update_fields=["stock_quantity", "updated_at"])

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level
