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

    def test_complete_delivery_workflow(self):
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

            self.assertEqual(
                delivery.status,
                DeliveryOrder.Status.PENDING,
            )

            delivery = DeliveryService.assign_delivery(
                delivery_id=delivery.id,
                user=self.user,
            )

            self.assertEqual(
                delivery.status,
                DeliveryOrder.Status.ASSIGNED,
            )

            self.assertEqual(
                delivery.assigned_to,
                self.user,
            )

            delivery = DeliveryService.start_delivery(
                delivery_id=delivery.id,
            )

            self.assertEqual(
                delivery.status,
                DeliveryOrder.Status.OUT_FOR_DELIVERY,
            )

            delivery = DeliveryService.complete_delivery(
                delivery_id=delivery.id,
            )

            self.assertEqual(
                delivery.status,
                DeliveryOrder.Status.DELIVERED,
            )

            self.assertIsNotNone(
                delivery.delivered_at,
            )

    def test_cannot_start_pending_delivery(self):
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

            with self.assertRaisesMessage(
                ValueError,
                "Only assigned delivery orders can go out for delivery.",
            ):
                DeliveryService.start_delivery(
                    delivery_id=delivery.id,
                )

    def test_cannot_complete_pending_delivery(self):
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

            with self.assertRaisesMessage(
                ValueError,
                "Only orders out for delivery can be marked as delivered.",
            ):
                DeliveryService.complete_delivery(
                    delivery_id=delivery.id,
                )
