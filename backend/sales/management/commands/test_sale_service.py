from django.core.management.base import BaseCommand

from sales.models import Sale
from sales.services import SaleService


class Command(BaseCommand):
    help = "Test sale completion and stock deduction."

    def handle(self, *args, **options):
        sale = (
            Sale.objects
            .filter(status=Sale.Status.DRAFT)
            .order_by("-created_at")
            .first()
        )

        if not sale:
            self.stdout.write(
                self.style.ERROR(
                    "No draft sale exists."
                )
            )
            return

        try:
            completed_sale = SaleService.complete_sale(
                sale_id=sale.id,
                user=sale.created_by,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Sale {completed_sale.invoice_number} "
                    f"completed successfully."
                )
            )

            self.stdout.write(
                f"Subtotal: KSh {completed_sale.subtotal}"
            )

            self.stdout.write(
                f"Total: KSh {completed_sale.total_amount}"
            )

            self.stdout.write(
                f"Total cost: KSh {completed_sale.total_cost}"
            )

            self.stdout.write(
                f"Gross profit: KSh "
                f"{completed_sale.gross_profit}"
            )

        except ValueError as error:
            self.stdout.write(
                self.style.ERROR(str(error))
            )
