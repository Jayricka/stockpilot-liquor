from django.urls import reverse
from rest_framework.test import APITestCase

from billing.models import Payment, Plan, Subscription
from billing.services.payments import PaymentService
from businesses.models import Business


class MpesaCallbackAPITestCase(APITestCase):

    def setUp(self):
        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.STARTER,
        )

        self.subscription = Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=Subscription.Status.ACTIVE,
        )

        self.payment = PaymentService.create_payment(
            subscription=self.subscription,
            amount=1500,
            phone_number="0712345678",
        )

        self.payment.checkout_request_id = (
            "ws_CO_123456789"
        )
        self.payment.merchant_request_id = (
            "29115-34620561-1"
        )
        self.payment.save(
            update_fields=[
                "checkout_request_id",
                "merchant_request_id",
            ]
        )

    def callback_url(self):
        return reverse("mpesa-callback")

    def success_payload(self):
        return {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": (
                        "29115-34620561-1"
                    ),
                    "CheckoutRequestID": (
                        "ws_CO_123456789"
                    ),
                    "ResultCode": 0,
                    "ResultDesc": (
                        "The service request is "
                        "processed successfully."
                    ),
                    "CallbackMetadata": {
                        "Item": [
                            {
                                "Name": "Amount",
                                "Value": 1500,
                            },
                            {
                                "Name": (
                                    "MpesaReceiptNumber"
                                ),
                                "Value": "QWE123456",
                            },
                            {
                                "Name": "TransactionDate",
                                "Value": 20261001203045,
                            },
                            {
                                "Name": "PhoneNumber",
                                "Value": 254712345678,
                            },
                        ],
                    },
                }
            }
        }

    def failure_payload(self):
        return {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": (
                        "29115-34620561-1"
                    ),
                    "CheckoutRequestID": (
                        "ws_CO_123456789"
                    ),
                    "ResultCode": 1032,
                    "ResultDesc": (
                        "Request cancelled by user."
                    ),
                }
            }
        }

    def test_success_callback_returns_200(self):
        response = self.client.post(
            self.callback_url(),
            self.success_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.SUCCESS,
        )
        self.assertEqual(
            self.payment.mpesa_receipt,
            "QWE123456",
        )

    def test_failure_callback_returns_200(self):
        response = self.client.post(
            self.callback_url(),
            self.failure_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.FAILED,
        )

    def test_callback_does_not_require_authentication(
        self,
    ):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.callback_url(),
            self.success_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_unknown_payment_returns_200(self):
        payload = self.success_payload()

        payload["Body"]["stkCallback"][
            "CheckoutRequestID"
        ] = "unknown-checkout-id"

        response = self.client.post(
            self.callback_url(),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_duplicate_callback_returns_200(self):
        first_response = self.client.post(
            self.callback_url(),
            self.success_payload(),
            format="json",
        )

        second_response = self.client.post(
            self.callback_url(),
            self.success_payload(),
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            200,
        )
        self.assertEqual(
            second_response.status_code,
            200,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.SUCCESS,
        )

    def test_invalid_payload_returns_400(self):
        response = self.client.post(
            self.callback_url(),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_callback_rejects_get_request(self):
        response = self.client.get(
            self.callback_url()
        )

        self.assertEqual(
            response.status_code,
            405,
        )
