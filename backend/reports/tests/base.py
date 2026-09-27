from decimal import Decimal

from django.utils import timezone
from rest_framework.test import APITestCase

from accounts.models import User
from businesses.models import Business, BusinessMembership
from deliveries.models import DeliveryOrder
from inventory.models import Purchase, PurchaseItem
from products.models import Category, Product
from sales.models import Sale, SaleItem
from suppliers.models import Supplier


class DashboardTestBase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@test.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="Owner",
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="TestPassword123!",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        self.other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        BusinessMembership.objects.create(
            user=self.owner,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        BusinessMembership.objects.create(
            user=self.other_user,
            business=self.other_business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        self.category = Category.objects.create(
            business=self.business,
            name="Spirits",
        )

        self.product = Product.objects.create(
            business=self.business,
            category=self.category,
            name="Test Vodka",
            sku="VOD-001",
            unit=Product.Unit.BOTTLE,
            buying_price=Decimal("1000.00"),
            selling_price=Decimal("1500.00"),
            stock_quantity=Decimal("10.00"),
            reorder_level=Decimal("3.00"),
        )

        self.low_stock_product = Product.objects.create(
            business=self.business,
            category=self.category,
            name="Low Stock Gin",
            sku="GIN-001",
            unit=Product.Unit.BOTTLE,
            buying_price=Decimal("800.00"),
            selling_price=Decimal("1200.00"),
            stock_quantity=Decimal("2.00"),
            reorder_level=Decimal("5.00"),
        )

        self.other_category = Category.objects.create(
            business=self.other_business,
            name="Other Spirits",
        )

        Product.objects.create(
            business=self.other_business,
            category=self.other_category,
            name="Other Vodka",
            sku="OTHER-001",
            unit=Product.Unit.BOTTLE,
            buying_price=Decimal("900.00"),
            selling_price=Decimal("1300.00"),
            stock_quantity=Decimal("20.00"),
            reorder_level=Decimal("5.00"),
        )

        self.sale = Sale.objects.create(
            business=self.business,
            created_by=self.owner,
            invoice_number="INV-001",
            payment_method=Sale.PaymentMethod.MPESA,
            status=Sale.Status.COMPLETED,
            sale_date=timezone.now(),
            subtotal=Decimal("3000.00"),
            total_amount=Decimal("3000.00"),
            total_cost=Decimal("2000.00"),
            gross_profit=Decimal("1000.00"),
        )

        SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("2.00"),
            unit_price=Decimal("1500.00"),
            unit_cost=Decimal("1000.00"),
        )

        self.supplier = Supplier.objects.create(
            business=self.business,
            name="Test Supplier",
            phone="0711223344",
        )

        self.purchase = Purchase.objects.create(
            business=self.business,
            supplier=self.supplier,
            created_by=self.owner,
            reference_number="PUR-001",
            status=Purchase.Status.COMPLETED,
            purchase_date=timezone.now(),
            total_amount=Decimal("2000.00"),
        )

        PurchaseItem.objects.create(
            purchase=self.purchase,
            product=self.product,
            quantity=Decimal("2.00"),
            unit_cost=Decimal("1000.00"),
        )

        self.delivery = DeliveryOrder.objects.create(
            business=self.business,
            sale=self.sale,
            customer_name="Test Customer",
            customer_phone="0700000000",
            delivery_address="Nairobi",
            delivery_fee=Decimal("200.00"),
            status=DeliveryOrder.Status.PENDING,
        )

        self.url = self.dashboard_url(self.business.id)

    def authenticate(self):
        self.client.force_authenticate(
            user=self.owner,
        )

    def dashboard_url(self, business_id):
        from django.urls import reverse

        return reverse(
            "dashboard",
            kwargs={
                "business_id": business_id,
            },
        )
