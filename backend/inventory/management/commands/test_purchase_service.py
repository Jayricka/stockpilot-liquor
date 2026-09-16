from django.core.management.base import BaseCommand

from accounts.models import User
from inventory.models import Purchase
from inventory.services import PurchaseService


class Command(BaseCommand):
    help = "Test purchase completion and stock updates."

    def handle(self, *args, **options):
        purchase = (
            Purchase.objects
            .filter(status=Purchase.Status.DRAFT)
            .order_by("-created_at")
            .first()
        )

        if not purchase:
            self.stdout.write(
                self.style.ERROR(
                    "No draft purchase exists."
                )
            )
            return

        user = purchase.created_by

        try:
            PurchaseService.complete_purchase(
                purchase_id=purchase.id,
                user=user,
            )

            purchase.refresh_from_db()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Purchase {purchase.reference_number} "
                    f"completed successfully."
                )
            )

            self.stdout.write(
                f"Total: KSh {purchase.total_amount}"
            )

        except ValueError as error:
            self.stdout.write(
                self.style.ERROR(str(error))
            )
