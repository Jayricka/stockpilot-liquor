from unittest.mock import patch

from django.utils import timezone
from rest_framework.test import APITestCase

from billing.models import Payment, Plan, Subscription
from billing.services.mpesa_callbacks import MpesaCallbackService
from billing.services.payments import PaymentService
from businesses.models import Business


class MpesaCallbackServiceTestCase(APITestCase):

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

    def test_success_callback_marks_payment_successful(
        self,
    ):
        result = MpesaCallbackService.process_callback(
            self.success_payload()
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            result,
            self.payment,
        )
        self.assertEqual(
            self.payment.status,
            Payment.Status.SUCCESS,
        )
        self.assertEqual(
            self.payment.mpesa_receipt,
            "QWE123456",
        )
        self.assertEqual(
            self.payment.result_code,
            0,
        )
        self.assertEqual(
            self.payment.result_description,
            (
                "The service request is "
                "processed successfully."
            ),
        )
        self.assertIsNotNone(
            self.payment.completed_at,
        )

    def test_failure_callback_marks_payment_failed(
        self,
    ):
        result = MpesaCallbackService.process_callback(
            self.failure_payload()
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            result,
            self.payment,
        )
        self.assertEqual(
            self.payment.status,
            Payment.Status.FAILED,
        )
        self.assertEqual(
            self.payment.mpesa_receipt,
            "",
        )
        self.assertEqual(
            self.payment.result_code,
            1032,
        )
        self.assertEqual(
            self.payment.result_description,
            "Request cancelled by user.",
        )
        self.assertIsNotNone(
            self.payment.completed_at,
        )

    def test_success_callback_uses_checkout_request_id(
        self,
    ):
        payload = self.success_payload()

        with patch.object(
            PaymentService,
            "mark_success",
            wraps=PaymentService.mark_success,
        ) as mock_mark_success:
            MpesaCallbackService.process_callback(
                payload
            )

        mock_mark_success.assert_called_once()

        mock_mark_success.assert_called_once_with(
            payment=self.payment,
            mpesa_receipt="QWE123456",
            result_code=0,
            result_description=(
                "The service request is "
                "processed successfully."
            ),
        )

    def test_unknown_checkout_request_is_ignored(
        self,
    ):
        payload = self.success_payload()

        payload["Body"]["stkCallback"][
            "CheckoutRequestID"
        ] = "unknown-checkout-id"

        result = MpesaCallbackService.process_callback(
            payload
        )

        self.assertIsNone(result)

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.PENDING,
        )

    def test_duplicate_success_callback_is_idempotent(
        self,
    ):
        MpesaCallbackService.process_callback(
            self.success_payload()
        )

        self.payment.refresh_from_db()

        completed_at = self.payment.completed_at

        result = MpesaCallbackService.process_callback(
            self.success_payload()
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            result,
            self.payment,
        )
        self.assertEqual(
            self.payment.status,
            Payment.Status.SUCCESS,
        )
        self.assertEqual(
            self.payment.completed_at,
            completed_at,
        )

    def test_duplicate_failure_callback_is_idempotent(
        self,
    ):
        MpesaCallbackService.process_callback(
            self.failure_payload()
        )

        self.payment.refresh_from_db()

        completed_at = self.payment.completed_at

        result = MpesaCallbackService.process_callback(
            self.failure_payload()
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            result,
            self.payment,
        )
        self.assertEqual(
            self.payment.status,
            Payment.Status.FAILED,
        )
        self.assertEqual(
            self.payment.completed_at,
            completed_at,
        )

    def test_callback_rejects_missing_body(self):
        with self.assertRaisesMessage(
            ValueError,
            "Invalid M-Pesa callback payload.",
        ):
            MpesaCallbackService.process_callback({})

    def test_callback_rejects_missing_stk_callback(
        self,
    ):
        payload = {
            "Body": {},
        }

        with self.assertRaisesMessage(
            ValueError,
            "Invalid M-Pesa callback payload.",
        ):
            MpesaCallbackService.process_callback(
                payload
            )

    def test_callback_rejects_missing_checkout_request_id(
        self,
    ):
        payload = self.success_payload()

        del payload["Body"]["stkCallback"][
            "CheckoutRequestID"
        ]

        with self.assertRaisesMessage(
            ValueError,
            "CheckoutRequestID is required.",
        ):
            MpesaCallbackService.process_callback(
                payload
            )

    def test_callback_rejects_missing_result_code(
        self,
    ):
        payload = self.success_payload()

        del payload["Body"]["stkCallback"][
            "ResultCode"
        ]

        with self.assertRaisesMessage(
            ValueError,
            "ResultCode is required.",
        ):
            MpesaCallbackService.process_callback(
                payload
            )

    def test_success_callback_requires_receipt(
        self,
    ):
        payload = self.success_payload()

        del payload["Body"]["stkCallback"][
            "CallbackMetadata"
        ]

        with self.assertRaisesMessage(
            ValueError,
            "M-Pesa receipt is required for "
            "successful payments.",
        ):
            MpesaCallbackService.process_callback(
                payload
            )
