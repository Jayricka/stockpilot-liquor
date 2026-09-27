from .base import AccountsTestBase


class AccountsAccessTests(AccountsTestBase):
    def test_register_is_public(self):
        self.client.logout()

        response = self.client.post(
            self.register_url,
            {
                "email": "public@example.com",
                "first_name": "Public",
                "last_name": "User",
                "password": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_login_is_public(self):
        self.client.logout()

        response = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_me_requires_authentication(self):
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, 401)

    def test_me_patch_requires_authentication(self):
        response = self.client.patch(
            self.me_url,
            {"first_name": "Updated"},
        )

        self.assertEqual(response.status_code, 401)
