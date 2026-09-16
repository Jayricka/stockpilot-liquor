from django.db import transaction
from django.utils import timezone

from .models import DeliveryOrder


class DeliveryService:
    @staticmethod
    @transaction.atomic
    def assign_delivery(delivery_id, user):
        delivery = (
            DeliveryOrder.objects
            .select_for_update()
            .select_related("business", "sale")
            .get(id=delivery_id)
        )

        if delivery.status in {
            DeliveryOrder.Status.DELIVERED,
            DeliveryOrder.Status.CANCELLED,
        }:
            raise ValueError(
                "A delivered or cancelled order cannot be assigned."
            )

        if user is None:
            raise ValueError("A delivery order must be assigned to a user.")

        if not user.is_active:
            raise ValueError("An inactive user cannot be assigned deliveries.")

        if not delivery.business.memberships.filter(
            user=user,
            is_active=True,
        ).exists():
            raise ValueError(
                "The assigned user is not an active member of this business."
            )

        delivery.assigned_to = user
        delivery.status = DeliveryOrder.Status.ASSIGNED
        delivery.assigned_at = timezone.now()

        delivery.save(
            update_fields=[
                "assigned_to",
                "status",
                "assigned_at",
                "updated_at",
            ]
        )

        return delivery

    @staticmethod
    @transaction.atomic
    def start_delivery(delivery_id):
        delivery = DeliveryOrder.objects.select_for_update().get(
            id=delivery_id
        )

        if delivery.status != DeliveryOrder.Status.ASSIGNED:
            raise ValueError(
                "Only assigned delivery orders can go out for delivery."
            )

        delivery.status = DeliveryOrder.Status.OUT_FOR_DELIVERY
        delivery.save(update_fields=["status", "updated_at"])

        return delivery

    @staticmethod
    @transaction.atomic
    def complete_delivery(delivery_id):
        delivery = DeliveryOrder.objects.select_for_update().get(
            id=delivery_id
        )

        if delivery.status != DeliveryOrder.Status.OUT_FOR_DELIVERY:
            raise ValueError(
                "Only orders out for delivery can be marked as delivered."
            )

        delivery.status = DeliveryOrder.Status.DELIVERED
        delivery.delivered_at = timezone.now()

        delivery.save(
            update_fields=[
                "status",
                "delivered_at",
                "updated_at",
            ]
        )

        return delivery

    @staticmethod
    @transaction.atomic
    def cancel_delivery(delivery_id):
        delivery = DeliveryOrder.objects.select_for_update().get(
            id=delivery_id
        )

        if delivery.status == DeliveryOrder.Status.DELIVERED:
            raise ValueError(
                "A delivered order cannot be cancelled."
            )

        if delivery.status == DeliveryOrder.Status.CANCELLED:
            raise ValueError(
                "This delivery order is already cancelled."
            )

        delivery.status = DeliveryOrder.Status.CANCELLED
        delivery.save(update_fields=["status", "updated_at"])

        return delivery
