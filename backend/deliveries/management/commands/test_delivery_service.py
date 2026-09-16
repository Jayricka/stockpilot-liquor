from django.core.management.base import BaseCommand

from accounts.models import User
from deliveries.models import DeliveryOrder
from deliveries.services import DeliveryService


class Command(BaseCommand):
    help = "Test the delivery order workflow."

    def handle(self, *args, **options):
        delivery = (
            DeliveryOrder.objects
            .filter(status=DeliveryOrder.Status.PENDING)
            .order_by("-created_at")
            .first()
        )

        if not delivery:
            self.stdout.write(
                self.style.ERROR("No pending delivery order exists.")
            )
            return

        user = (
            User.objects
            .filter(
                business_memberships__business=delivery.business,
                business_memberships__is_active=True,
            )
            .order_by("date_joined")
            .first()
        )

        if not user:
            self.stdout.write(
                self.style.ERROR(
                    "No active business member exists for this delivery."
                )
            )
            return

        try:
            assigned_delivery = DeliveryService.assign_delivery(
                delivery_id=delivery.id,
                user=user,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Delivery assigned to {assigned_delivery.assigned_to.email}."
                )
            )

            started_delivery = DeliveryService.start_delivery(
                delivery_id=assigned_delivery.id,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Delivery status: {started_delivery.get_status_display()}."
                )
            )

            completed_delivery = DeliveryService.complete_delivery(
                delivery_id=started_delivery.id,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Delivery {completed_delivery.id} completed successfully."
                )
            )
            self.stdout.write(
                f"Final status: {completed_delivery.get_status_display()}"
            )
            self.stdout.write(
                f"Delivered at: {completed_delivery.delivered_at}"
            )

        except ValueError as error:
            self.stdout.write(
                self.style.ERROR(str(error))
            )
