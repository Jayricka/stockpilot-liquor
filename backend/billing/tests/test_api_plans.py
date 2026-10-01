from django.urls import reverse
from rest_framework import status

from billing.models import Plan

from .base import BillingAPITestBase


class BillingPlansAPITest(BillingAPITestBase):

    def test_authenticated_user_can_list_active_plans(self):
        response = self.client.get(
            reverse("billing-plans")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            Plan.objects.filter(
                is_active=True,
            ).count(),
        )

    def test_plan_response_contains_expected_fields(self):
        response = self.client.get(
            reverse("billing-plans")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        plan = response.data[0]

        self.assertIn("code", plan)
        self.assertIn("name", plan)
        self.assertIn("price", plan)
        self.assertIn("currency", plan)
        self.assertIn("trial_days", plan)

    def test_inactive_plans_are_not_returned(self):
        Plan.objects.filter(
            code=Plan.Code.GROWTH,
        ).update(
            is_active=False,
        )

        response = self.client.get(
            reverse("billing-plans")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        codes = {
            plan["code"]
            for plan in response.data
        }

        self.assertNotIn(
            Plan.Code.GROWTH,
            codes,
        )

    def test_plans_endpoint_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse("billing-plans")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
