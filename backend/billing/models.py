from django.conf import settings
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    class Code(models.TextChoices):
        STARTER = "starter", "Starter"
        GROWTH = "growth", "Growth"
        BUSINESS = "business", "Business"

    code = models.CharField(
        max_length=20,
        choices=Code.choices,
        unique=True,
    )

    name = models.CharField(
        max_length=50,
    )

    price = models.PositiveIntegerField()

    currency = models.CharField(
        max_length=3,
        default="KES",
    )

    trial_days = models.PositiveSmallIntegerField(
        default=7,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} - {self.currency} {self.price}"


class Subscription(models.Model):
    class Status(models.TextChoices):
        TRIALING = "TRIALING", "Trialing"
        ACTIVE = "ACTIVE", "Active"
        PAST_DUE = "PAST_DUE", "Past due"
        CANCELLED = "CANCELLED", "Cancelled"
        EXPIRED = "EXPIRED", "Expired"

    business = models.OneToOneField(
        "businesses.Business",
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TRIALING,
    )

    trial_started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    trial_ends_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    current_period_start = models.DateTimeField(
        null=True,
        blank=True,
    )

    current_period_end = models.DateTimeField(
        null=True,
        blank=True,
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.business.name} - {self.plan.name}"

    @property
    def is_trial_active(self):
        return (
            self.status == self.Status.TRIALING
            and self.trial_ends_at is not None
            and timezone.now() < self.trial_ends_at
        )

    @property
    def trial_days_remaining(self):
        if not self.is_trial_active:
            return 0

        remaining = self.trial_ends_at - timezone.now()
        return max(0, remaining.days + 1)


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"
        EXPIRED = "EXPIRED", "Expired"

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    amount = models.PositiveIntegerField()

    currency = models.CharField(
        max_length=3,
        default="KES",
    )

    phone_number = models.CharField(
        max_length=20,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    merchant_request_id = models.CharField(
        max_length=100,
        blank=True,
    )

    checkout_request_id = models.CharField(
        max_length=100,
        blank=True,
    )

    mpesa_receipt = models.CharField(
        max_length=100,
        blank=True,
    )

    result_code = models.IntegerField(
        null=True,
        blank=True,
    )

    result_description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.subscription.business.name} - "
            f"{self.currency} {self.amount} - "
            f"{self.status}"
        )
