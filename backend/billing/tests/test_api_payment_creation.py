from django.urls import reverse

from billing.models import Payment, Subscription
from billing.tests.base import BillingAPITestBase


class PaymentCreationAPITestCase(BillingAPITestBase):

    def payment_url(self):
        return reverse(
            "business-payments",
            kwargs={
                "business_id": self.business.id,
            },
        )

    def test_member_can_create_payment(self):
        response = self.client.post(
            self.payment_url(),
            {
                "amount": 1500,
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        payment = Payment.objects.get(
            id=response.data["id"]
        )

        self.assertEqual(
            payment.subscription,
            self.subscription,
        )
        self.assertEqual(payment.amount, 1500)
        self.assertEqual(
            payment.currency,
            self.plan.currency,
        )
        self.assertEqual(
            payment.phone_number,
            "0712345678",
        )
        self.assertEqual(
            payment.status,
            Payment.Status.PENDING,
        )

    def test_payment_creation_rejects_zero_amount(self):
        response = self.client.post(
            self.payment_url(),
            {
                "amount": 0,
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("amount", response.data)

    def test_payment_creation_rejects_missing_amount(self):
        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("amount", response.data)

    def test_payment_creation_rejects_blank_phone_number(
        self,
    ):
        response = self.client.post(
            self.payment_url(),
            {
                "amount": 1500,
                "phone_number": "   ",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone_number", response.data)

    def test_payment_creation_rejects_cancelled_subscription(
        self,
    ):
        self.subscription.status = (
            Subscription.Status.CANCELLED
        )
        self.subscription.save(
            update_fields=["status"]
        )

        response = self.client.post(
            self.payment_url(),
            {
                "amount": 1500,
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["detail"],
            (
                "Payments cannot be created for "
                "this subscription."
            ),
        )

    def test_payment_creation_rejects_expired_subscription(
        self,
    ):
        self.subscription.status = (
            Subscription.Status.EXPIRED
        )
        self.subscription.save(
            update_fields=["status"]
        )

        response = self.client.post(
            self.payment_url(),
            {
                "amount": 1500,
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_payment_creation_rejects_other_business(
        self,
    ):
        other_business = self.business.__class__.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        url = reverse(
            "business-payments",
            kwargs={
                "business_id": other_business.id,
            },
        )

        response = self.client.post(
            url,
            {
                "amount": 1500,
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_payment_creation_requires_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.payment_url(),
            {
                "amount": 1500,
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_payment_creation_does_not_accept_status(
        self,
    ):
        response = self.client.post(
            self.payment_url(),
            {
                "amount": 1500,
                "phone_number": "0712345678",
                "status": Payment.Status.SUCCESS,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["status"],
            Payment.Status.PENDING,
        )

    def test_payment_creation_does_not_accept_receipt(
        self,
    ):
        response = self.client.post(
            self.payment_url(),
            {
                "amount": 1500,
                "phone_number": "0712345678",
                "mpesa_receipt": "FAKE123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["status"],
            Payment.Status.PENDING,
        )
        self.assertEqual(
            response.data["mpesa_receipt"],
            "",
        )

    def test_payment_creation_preserves_subscription(
        self,
    ):
        original_status = self.subscription.status

        self.client.post(
            self.payment_url(),
            {
                "amount": 1500,
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.subscription.refresh_from_db()

        self.assertEqual(
            self.subscription.status,
            original_status,
        )
