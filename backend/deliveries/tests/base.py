from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from businesses.models import Business, BusinessMembership
from deliveries.models import DeliveryOrder
from deliveries.services import DeliveryService
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
