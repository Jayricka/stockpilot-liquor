from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from businesses.models import Business, BusinessMembership
from deliveries.models import DeliveryOrder
from deliveries.services import DeliveryService
from sales.models import Sale

from .base import DeliveryServiceTestBase


class DeliveryServiceTests(DeliveryServiceTestBase):

    def test_create_delivery_for_completed_sale(self):
            delivery = DeliveryService.create_delivery(
                business=self.business,
                user=self.user,
                validated_data={
                    "sale": self.sale,
                    "customer_name": "John Doe",
                    "customer_phone": "0712345678",
                    "delivery_address": "Kilimani, Nairobi",
                    "delivery_fee": Decimal("200.00"),
                    "notes": "Call before delivery.",
                },
            )

            self.assertEqual(
                delivery.status,
                DeliveryOrder.Status.PENDING,
            )

            self.assertEqual(
                delivery.sale,
                self.sale,
            )

            self.assertEqual(
                delivery.delivery_fee,
                Decimal("200.00"),
            )

    def test_cannot_create_delivery_for_incomplete_sale(self):
            draft_sale = Sale.objects.create(
                business=self.business,
                created_by=self.user,
                invoice_number="TEST-INV-002",
                payment_method=Sale.PaymentMethod.CASH,
                status=Sale.Status.DRAFT,
                sale_date=timezone.now(),
            )

            with self.assertRaisesMessage(
                ValueError,
                "Only completed sales can have delivery orders.",
            ):
                DeliveryService.create_delivery(
                    business=self.business,
                    user=self.user,
                    validated_data={
                        "sale": draft_sale,
                        "customer_name": "Jane Doe",
                        "customer_phone": "0799999999",
                        "delivery_address": "Westlands, Nairobi",
                        "delivery_fee": Decimal("150.00"),
                    },
                )
