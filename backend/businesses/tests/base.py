from rest_framework.test import APITestCase

from accounts.models import User


class BusinessOnboardingTestBase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            first_name="John",
            last_name="Owner",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.url = self.get_onboarding_url()

    def get_onboarding_url(self):
        from django.urls import reverse

        return reverse("business-onboard")

    def payload(self, plan="starter"):
        return {
            "name": "Ricka Liquor Store",
            "business_type": "liquor_store",
            "phone": "0712345678",
            "email": "store@example.com",
            "address": "Nairobi",
            "license_number": "LIC-12345",
            "plan": plan,
        }
