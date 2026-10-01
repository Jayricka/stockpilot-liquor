from django.urls import reverse
from rest_framework import status

from billing.models import Payment
from businesses.models import Business

from .base import BillingAPITestBase


class PaymentListAPITests(BillingAPITestBase):

    def setUp(self):
        super().setUp()

        self.payment = Payment.objects.create(
            subscription=self.subscription,
            amount=1500,
            currency="KES",
            phone_number="0712345678",
            status=Payment.Status.SUCCESS,
            mpesa_receipt="QWE123456",
        )

    def test_business_member_can_list_payments(self):
        response = self.client.get(
            reverse(
                "business-payments",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            1,
        )

    def test_payment_returns_expected_fields(self):
        response = self.client.get(
            reverse(
                "business-payments",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        payment = response.data[0]

        self.assertEqual(
            payment["id"],
            self.payment.id,
        )
        self.assertEqual(
            payment["amount"],
            1500,
        )
        self.assertEqual(
            payment["currency"],
            "KES",
        )
        self.assertEqual(
            payment["phone_number"],
            "0712345678",
        )
        self.assertEqual(
            payment["status"],
            Payment.Status.SUCCESS,
        )
        self.assertEqual(
            payment["mpesa_receipt"],
            "QWE123456",
        )

    def test_user_cannot_access_another_business_payments(self):
        other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        response = self.client.get(
            reverse(
                "business-payments",
                kwargs={
                    "business_id": other_business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_list_payments(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            reverse(
                "business-payments",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
