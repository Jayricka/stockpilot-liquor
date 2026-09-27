from rest_framework import status

from .base import DashboardTestBase


class DashboardAccessAPITests(DashboardTestBase):

    def test_dashboard_is_business_isolated(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_text = str(response.data)

        self.assertNotIn(
            "Other Vodka",
            response_text,
        )

    def test_user_cannot_access_another_business_dashboard(self):
        self.authenticate()

        url = self.dashboard_url(
            self.other_business.id,
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
