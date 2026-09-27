from .base import AccountsTestBase


class LoginAPITests(AccountsTestBase):
    def login_data(self):
        return {
            "email": self.user.email,
            "password": self.password,
        }

    def test_login_user(self):
        response = self.client.post(
            self.login_url,
            self.login_data(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_returns_expected_user_data(self):
        response = self.client.post(
            self.login_url,
            self.login_data(),
        )

        user_data = response.data["user"]

        self.assertEqual(
            user_data["email"],
            self.user.email,
        )
        self.assertEqual(
            user_data["first_name"],
            "Test",
        )
        self.assertEqual(
            user_data["last_name"],
            "User",
        )
        self.assertEqual(
            user_data["full_name"],
            "Test User",
        )

    def test_login_with_invalid_password(self):
        data = self.login_data()
        data["password"] = "WrongPassword123!"

        response = self.client.post(
            self.login_url,
            data,
        )

        self.assertEqual(response.status_code, 400)

    def test_login_with_unknown_email(self):
        data = self.login_data()
        data["email"] = "unknown@example.com"

        response = self.client.post(
            self.login_url,
            data,
        )

        self.assertEqual(response.status_code, 400)

    def test_inactive_user_cannot_login(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            self.login_url,
            self.login_data(),
        )

        self.assertEqual(response.status_code, 400)
