from rest_framework.test import APITestCase

from accounts.models import User


class AccountsTestBase(APITestCase):
    register_url = "/api/auth/register/"
    login_url = "/api/auth/login/"
    me_url = "/api/auth/me/"

    def setUp(self):
        self.password = "StrongPass123!"

        self.user = User.objects.create_user(
            email="test@example.com",
            password=self.password,
            first_name="Test",
            last_name="User",
        )
