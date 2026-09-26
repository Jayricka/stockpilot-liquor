from rest_framework import status

from .base import PurchaseAPITestBase


class PurchasePermissionsApiTests(PurchaseAPITestBase):

    def test_unauthenticated_access_is_rejected(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

