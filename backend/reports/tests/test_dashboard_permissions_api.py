from django.urls import reverse
from rest_framework import status

from .base import DashboardAPITestBase


class DashboardPermissionsApiTests(DashboardAPITestBase):

    def test_user_cannot_access_another_business_dashboard(self):
        self.authenticate()

        url = reverse(
            "dashboard",
            kwargs={
                "business_id": self.other_business.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_access_dashboard(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

