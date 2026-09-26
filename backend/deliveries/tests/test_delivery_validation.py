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

    def test_cannot_create_duplicate_delivery(self):
            DeliveryService.create_delivery(
                business=self.business,
                user=self.user,
                validated_data={
                    "sale": self.sale,
                    "customer_name": "John Doe",
                    "customer_phone": "0712345678",
                    "delivery_address": "Kilimani, Nairobi",
                    "delivery_fee": Decimal("200.00"),
                },
            )

            with self.assertRaisesMessage(
                ValueError,
                "This sale already has a delivery order.",
            ):
                DeliveryService.create_delivery(
                    business=self.business,
                    user=self.user,
                    validated_data={
                        "sale": self.sale,
                        "customer_name": "John Doe",
                        "customer_phone": "0712345678",
                        "delivery_address": "Kilimani, Nairobi",
                        "delivery_fee": Decimal("200.00"),
                    },
                )

    def test_cannot_assign_delivery_to_non_member(self):
            delivery = DeliveryService.create_delivery(
                business=self.business,
                user=self.user,
                validated_data={
                    "sale": self.sale,
                    "customer_name": "John Doe",
                    "customer_phone": "0712345678",
                    "delivery_address": "Kilimani, Nairobi",
                    "delivery_fee": Decimal("200.00"),
                },
            )

            outsider = User.objects.create_user(
                email="outsider@test.com",
                password="TestPassword123!",
            )

            with self.assertRaisesMessage(
                ValueError,
                "The assigned user is not an active member of this business.",
            ):
                DeliveryService.assign_delivery(
                    delivery_id=delivery.id,
                    user=outsider,
                )

    def test_cannot_cancel_delivered_delivery(self):
            delivery = DeliveryService.create_delivery(
                business=self.business,
                user=self.user,
                validated_data={
                    "sale": self.sale,
                    "customer_name": "John Doe",
                    "customer_phone": "0712345678",
                    "delivery_address": "Kilimani, Nairobi",
                    "delivery_fee": Decimal("200.00"),
                },
            )

            DeliveryService.assign_delivery(
                delivery_id=delivery.id,
                user=self.user,
            )

            DeliveryService.start_delivery(
                delivery_id=delivery.id,
            )

            DeliveryService.complete_delivery(
                delivery_id=delivery.id,
            )

            with self.assertRaisesMessage(
                ValueError,
                "A delivered order cannot be cancelled.",
            ):
                DeliveryService.cancel_delivery(
                    delivery_id=delivery.id,
                )
