from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from businesses.models import Business, BusinessMembership
from sales.models import Sale


class DeliveryServiceTestBase(TestCase):
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

    def delivery_data(self):
        return {
            "sale": self.sale,
            "customer_name": "John Doe",
            "customer_phone": "0712345678",
            "delivery_address": "Kilimani, Nairobi",
            "delivery_fee": Decimal("200.00"),
        }

    def create_delivery(self):
        from deliveries.services import DeliveryService

        return DeliveryService.create_delivery(
            business=self.business,
            user=self.user,
            validated_data=self.delivery_data(),
        )
