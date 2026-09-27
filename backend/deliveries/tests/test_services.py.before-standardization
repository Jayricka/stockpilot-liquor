from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from businesses.models import Business, BusinessMembership
from deliveries.models import DeliveryOrder
from deliveries.services import DeliveryService
from sales.models import Sale


class DeliveryServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@test.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="Owner",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        self.sale = Sale.objects.create(
            business=self.business,
            created_by=self.user,
            invoice_number="TEST-INV-001",
            payment_method=Sale.PaymentMethod.MPESA,
            status=Sale.Status.COMPLETED,
            sale_date=timezone.now(),
            subtotal=Decimal("2200.00"),
            total_amount=Decimal("2200.00"),
            total_cost=Decimal("1700.00"),
            gross_profit=Decimal("500.00"),
        )

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
