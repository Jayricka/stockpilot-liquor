from deliveries.models import DeliveryOrder
from deliveries.services import DeliveryService

from .base import DeliveryServiceTestBase


class DeliveryServiceWorkflowTests(DeliveryServiceTestBase):
    def test_complete_delivery_workflow(self):
        delivery = self.create_delivery()

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
        delivery = self.create_delivery()

        with self.assertRaisesMessage(
            ValueError,
            "Only assigned delivery orders can go out for delivery.",
        ):
            DeliveryService.start_delivery(
                delivery_id=delivery.id,
            )

    def test_cannot_complete_pending_delivery(self):
        delivery = self.create_delivery()

        with self.assertRaisesMessage(
            ValueError,
            "Only orders out for delivery can be marked as delivered.",
        ):
            DeliveryService.complete_delivery(
                delivery_id=delivery.id,
            )

    def test_cannot_cancel_delivered_delivery(self):
        delivery = self.create_delivery()

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
