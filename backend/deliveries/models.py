from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class DeliveryOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ASSIGNED = "ASSIGNED", "Assigned"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for delivery"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    business = models.ForeignKey(
        "businesses.Business",
        on_delete=models.CASCADE,
        related_name="delivery_orders",
    )

    sale = models.OneToOneField(
        "sales.Sale",
        on_delete=models.PROTECT,
        related_name="delivery_order",
    )

    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=30)
    delivery_address = models.TextField()

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assigned_deliveries",
        null=True,
        blank=True,
    )

    delivery_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    notes = models.TextField(blank=True)

    assigned_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Delivery order"
        verbose_name_plural = "Delivery orders"

    def __str__(self):
        return f"{self.customer_name} - {self.sale.invoice_number}"

    def assign_to(self, user):
        if self.status in {
            self.Status.DELIVERED,
            self.Status.CANCELLED,
        }:
            raise ValueError(
                "A delivered or cancelled order cannot be assigned."
            )

        if user is None:
            raise ValueError("A delivery order must be assigned to a user.")

        if user.id is None:
            raise ValueError("The assigned user must be saved.")

        self.assigned_to = user
        self.status = self.Status.ASSIGNED
        self.assigned_at = timezone.now()
        self.save(
            update_fields=[
                "assigned_to",
                "status",
                "assigned_at",
                "updated_at",
            ]
        )

    def mark_out_for_delivery(self):
        if self.status != self.Status.ASSIGNED:
            raise ValueError(
                "Only assigned delivery orders can go out for delivery."
            )

        self.status = self.Status.OUT_FOR_DELIVERY
        self.save(update_fields=["status", "updated_at"])

    def mark_delivered(self):
        if self.status != self.Status.OUT_FOR_DELIVERY:
            raise ValueError(
                "Only orders out for delivery can be marked as delivered."
            )

        self.status = self.Status.DELIVERED
        self.delivered_at = timezone.now()
        self.save(update_fields=["status", "delivered_at", "updated_at"])

    def cancel(self):
        if self.status == self.Status.DELIVERED:
            raise ValueError(
                "A delivered order cannot be cancelled."
            )

        self.status = self.Status.CANCELLED
        self.save(update_fields=["status", "updated_at"])
