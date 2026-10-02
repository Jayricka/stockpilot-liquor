import base64

import requests
from django.conf import settings
from django.utils import timezone


class MpesaGatewayError(Exception):
    """Raised when a Daraja API request fails."""


class MpesaGateway:
    """Gateway for communicating with Safaricom Daraja APIs."""

    def __init__(self):
        self.environment = settings.MPESA_ENVIRONMENT

        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL

        self.transaction_type = (
            settings.MPESA_TRANSACTION_TYPE
        )
        self.account_reference = (
            settings.MPESA_ACCOUNT_REFERENCE
        )
        self.transaction_description = (
            settings.MPESA_TRANSACTION_DESCRIPTION
        )

        if self.environment == "production":
            self.base_url = (
                "https://api.safaricom.co.ke"
            )
        else:
            self.base_url = (
                "https://sandbox.safaricom.co.ke"
            )

    def get_access_token(self):
        """Request an OAuth access token from Daraja."""
        credentials = (
            f"{self.consumer_key}:"
            f"{self.consumer_secret}"
        )

        encoded_credentials = base64.b64encode(
            credentials.encode()
        ).decode()

        response = requests.get(
            (
                f"{self.base_url}"
                "/oauth/v1/generate"
            ),
            params={
                "grant_type": "client_credentials",
            },
            headers={
                "Authorization": (
                    f"Basic {encoded_credentials}"
                ),
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        try:
            return data["access_token"]
        except KeyError as exc:
            raise MpesaGatewayError(
                "Daraja response did not contain "
                "an access token."
            ) from exc

    def generate_timestamp(self):
        """Generate the Daraja transaction timestamp."""
        return timezone.localtime().strftime(
            "%Y%m%d%H%M%S"
        )

    def generate_password(self, timestamp):
        """Generate the Daraja STK password."""
        value = (
            f"{self.shortcode}"
            f"{self.passkey}"
            f"{timestamp}"
        )

        return base64.b64encode(
            value.encode()
        ).decode()

    def normalize_phone_number(self, phone_number):
        """Convert a Kenyan phone number to 254 format."""
        phone_number = phone_number.strip()

        if phone_number.startswith("+254"):
            return phone_number[1:]

        if phone_number.startswith("254"):
            return phone_number

        if phone_number.startswith("0"):
            return f"254{phone_number[1:]}"

        raise ValueError(
            "Phone number must be a valid Kenyan "
            "mobile number."
        )

    def stk_push(self, payment):
        """Initiate an M-Pesa Express STK Push."""
        if payment.currency != "KES":
            raise ValueError(
                "M-Pesa payments must use KES."
            )

        timestamp = self.generate_timestamp()
        password = self.generate_password(timestamp)
        access_token = self.get_access_token()

        phone_number = self.normalize_phone_number(
            payment.phone_number
        )

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": self.transaction_type,
            "Amount": payment.amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": (
                f"{self.account_reference}-{payment.id}"
            ),
            "TransactionDesc": (
                self.transaction_description
            ),
        }

        response = requests.post(
            (
                f"{self.base_url}"
                "/mpesa/stkpush/v1/processrequest"
            ),
            json=payload,
            headers={
                "Authorization": (
                    f"Bearer {access_token}"
                ),
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        response_code = data.get("ResponseCode")

        if response_code != "0":
            raise MpesaGatewayError(
                data.get(
                    "ResponseDescription",
                    "M-Pesa STK Push failed.",
                )
            )

        merchant_request_id = data.get(
            "MerchantRequestID"
        )
        checkout_request_id = data.get(
            "CheckoutRequestID"
        )

        if not merchant_request_id:
            raise MpesaGatewayError(
                "Daraja response did not contain "
                "a merchant request ID."
            )

        if not checkout_request_id:
            raise MpesaGatewayError(
                "Daraja response did not contain "
                "a checkout request ID."
            )

        return {
            "merchant_request_id": merchant_request_id,
            "checkout_request_id": checkout_request_id,
            "response_code": response_code,
            "response_description": data.get(
                "ResponseDescription",
                "",
            ),
            "customer_message": data.get(
                "CustomerMessage",
                "",
            ),
        }
