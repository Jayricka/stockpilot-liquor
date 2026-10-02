from unittest.mock import Mock, patch

from django.test import SimpleTestCase, override_settings

from billing.services.mpesa import (
    MpesaGateway,
    MpesaGatewayError,
)


@override_settings(
    MPESA_ENVIRONMENT="sandbox",
    MPESA_CONSUMER_KEY="test-key",
    MPESA_CONSUMER_SECRET="test-secret",
    MPESA_SHORTCODE="600000",
    MPESA_PASSKEY="test-passkey",
    MPESA_CALLBACK_URL=(
        "https://example.com/api/mpesa/callback/"
    ),
    MPESA_TRANSACTION_TYPE="CustomerPayBillOnline",
    MPESA_ACCOUNT_REFERENCE="StockPilot",
    MPESA_TRANSACTION_DESCRIPTION=(
        "StockPilot payment"
    ),
)
class MpesaGatewayTestCase(SimpleTestCase):

    def setUp(self):
        self.gateway = MpesaGateway()

    def test_gateway_uses_sandbox_environment(self):
        self.assertEqual(
            self.gateway.base_url,
            "https://sandbox.safaricom.co.ke",
        )

    @override_settings(
        MPESA_ENVIRONMENT="production",
    )
    def test_gateway_uses_production_environment(self):
        gateway = MpesaGateway()

        self.assertEqual(
            gateway.base_url,
            "https://api.safaricom.co.ke",
        )

    @patch("billing.services.mpesa.requests.get")
    def test_get_access_token(self, mock_get):
        response = Mock()
        response.json.return_value = {
            "access_token": "test-access-token",
            "expires_in": 3599,
        }

        mock_get.return_value = response

        token = self.gateway.get_access_token()

        self.assertEqual(
            token,
            "test-access-token",
        )

        mock_get.assert_called_once()
        response.raise_for_status.assert_called_once()

    @patch("billing.services.mpesa.requests.get")
    def test_get_access_token_sends_basic_auth(
        self,
        mock_get,
    ):
        response = Mock()
        response.json.return_value = {
            "access_token": "test-access-token",
        }

        mock_get.return_value = response

        self.gateway.get_access_token()

        call = mock_get.call_args

        self.assertEqual(
            call.kwargs["params"],
            {
                "grant_type": "client_credentials",
            },
        )

        self.assertTrue(
            call.kwargs["headers"][
                "Authorization"
            ].startswith("Basic ")
        )

        self.assertEqual(
            call.kwargs["timeout"],
            30,
        )

    @patch("billing.services.mpesa.requests.get")
    def test_get_access_token_raises_for_http_error(
        self,
        mock_get,
    ):
        response = Mock()
        mock_get.return_value = response

        response.raise_for_status.side_effect = (
            RuntimeError("Daraja unavailable")
        )

        with self.assertRaises(RuntimeError):
            self.gateway.get_access_token()

    def test_generate_timestamp(self):
        timestamp = self.gateway.generate_timestamp()

        self.assertEqual(
            len(timestamp),
            14,
        )

        self.assertTrue(
            timestamp.isdigit()
        )

    def test_generate_password(self):
        timestamp = "20261001195500"

        password = self.gateway.generate_password(
            timestamp
        )

        self.assertTrue(password)

    def test_normalize_local_phone_number(self):
        self.assertEqual(
            self.gateway.normalize_phone_number(
                "0712345678"
            ),
            "254712345678",
        )

    def test_normalize_plus_phone_number(self):
        self.assertEqual(
            self.gateway.normalize_phone_number(
                "+254712345678"
            ),
            "254712345678",
        )

    def test_normalize_international_phone_number(self):
        self.assertEqual(
            self.gateway.normalize_phone_number(
                "254712345678"
            ),
            "254712345678",
        )

    def test_reject_invalid_phone_number(self):
        with self.assertRaisesMessage(
            ValueError,
            (
                "Phone number must be a valid Kenyan "
                "mobile number."
            ),
        ):
            self.gateway.normalize_phone_number(
                "712345678"
            )

    @patch(
        "billing.services.mpesa.MpesaGateway."
        "get_access_token"
    )
    @patch("billing.services.mpesa.requests.post")
    def test_stk_push(
        self,
        mock_post,
        mock_get_access_token,
    ):
        payment = Mock()
        payment.id = 10
        payment.amount = 1500
        payment.currency = "KES"
        payment.phone_number = "0712345678"

        mock_get_access_token.return_value = (
            "test-access-token"
        )

        response = Mock()
        response.json.return_value = {
            "MerchantRequestID": "merchant-123",
            "CheckoutRequestID": "checkout-123",
            "ResponseCode": "0",
            "ResponseDescription": (
                "Success. Request accepted for processing"
            ),
            "CustomerMessage": (
                "Success. Request accepted for processing"
            ),
        }

        mock_post.return_value = response

        result = self.gateway.stk_push(payment)

        self.assertEqual(
            result["merchant_request_id"],
            "merchant-123",
        )
        self.assertEqual(
            result["checkout_request_id"],
            "checkout-123",
        )
        self.assertEqual(
            result["response_code"],
            "0",
        )

        mock_post.assert_called_once()

        call = mock_post.call_args

        self.assertEqual(
            call.kwargs["headers"]["Authorization"],
            "Bearer test-access-token",
        )

        payload = call.kwargs["json"]

        self.assertEqual(
            payload["BusinessShortCode"],
            "600000",
        )
        self.assertEqual(
            payload["Amount"],
            1500,
        )
        self.assertEqual(
            payload["PartyA"],
            "254712345678",
        )
        self.assertEqual(
            payload["PhoneNumber"],
            "254712345678",
        )
        self.assertEqual(
            payload["PartyB"],
            "600000",
        )
        self.assertEqual(
            payload["AccountReference"],
            "StockPilot-10",
        )
        self.assertEqual(
            payload["CallBackURL"],
            (
                "https://example.com/"
                "api/mpesa/callback/"
            ),
        )

    @patch(
        "billing.services.mpesa.MpesaGateway."
        "get_access_token"
    )
    @patch("billing.services.mpesa.requests.post")
    def test_stk_push_rejects_failed_response(
        self,
        mock_post,
        mock_get_access_token,
    ):
        payment = Mock()
        payment.id = 10
        payment.amount = 1500
        payment.currency = "KES"
        payment.phone_number = "0712345678"

        mock_get_access_token.return_value = (
            "test-access-token"
        )

        response = Mock()
        response.json.return_value = {
            "ResponseCode": "1",
            "ResponseDescription": (
                "Request rejected"
            ),
        }

        mock_post.return_value = response

        with self.assertRaisesMessage(
            MpesaGatewayError,
            "Request rejected",
        ):
            self.gateway.stk_push(payment)

    @patch(
        "billing.services.mpesa.MpesaGateway."
        "get_access_token"
    )
    @patch("billing.services.mpesa.requests.post")
    def test_stk_push_requires_merchant_request_id(
        self,
        mock_post,
        mock_get_access_token,
    ):
        payment = Mock()
        payment.id = 10
        payment.amount = 1500
        payment.currency = "KES"
        payment.phone_number = "0712345678"

        mock_get_access_token.return_value = (
            "test-access-token"
        )

        response = Mock()
        response.json.return_value = {
            "ResponseCode": "0",
            "ResponseDescription": "Accepted",
        }

        mock_post.return_value = response

        with self.assertRaisesMessage(
            MpesaGatewayError,
            (
                "Daraja response did not contain "
                "a merchant request ID."
            ),
        ):
            self.gateway.stk_push(payment)

    def test_stk_push_requires_kes(self):
        payment = Mock()
        payment.currency = "USD"

        with self.assertRaisesMessage(
            ValueError,
            "M-Pesa payments must use KES.",
        ):
            self.gateway.stk_push(payment)
