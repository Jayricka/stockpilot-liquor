from accounts.models import User

from .base import AccountsTestBase


class RegistrationAPITests(AccountsTestBase):
    def registration_data(self):
        return {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "StrongPass123!",
        }

    def test_register_user(self):
        response = self.client.post(
            self.register_url,
            self.registration_data(),
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("user", response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        self.assertTrue(
            User.objects.filter(
                email="new@example.com"
            ).exists()
        )

    def test_register_user_returns_expected_user_data(self):
        response = self.client.post(
            self.register_url,
            self.registration_data(),
        )

        user_data = response.data["user"]

        self.assertIn("id", user_data)
        self.assertEqual(
            user_data["email"],
            "new@example.com",
        )
        self.assertEqual(
            user_data["first_name"],
            "New",
        )
        self.assertEqual(
            user_data["last_name"],
            "User",
        )
        self.assertEqual(
            user_data["full_name"],
            "New User",
        )

    def test_register_user_password_is_not_returned(self):
        response = self.client.post(
            self.register_url,
            self.registration_data(),
        )

        self.assertNotIn(
            "password",
            response.data["user"],
        )

    def test_register_duplicate_email(self):
        data = self.registration_data()
        data["email"] = self.user.email

        response = self.client.post(
            self.register_url,
            data,
        )

        self.assertEqual(response.status_code, 400)

    def test_register_password_must_be_at_least_eight_characters(self):
        data = self.registration_data()
        data["password"] = "short"

        response = self.client.post(
            self.register_url,
            data,
        )

        self.assertEqual(response.status_code, 400)

    def test_register_requires_email(self):
        data = self.registration_data()
        data.pop("email")

        response = self.client.post(
            self.register_url,
            data,
        )

        self.assertEqual(response.status_code, 400)

    def test_register_requires_password(self):
        data = self.registration_data()
        data.pop("password")

        response = self.client.post(
            self.register_url,
            data,
        )

        self.assertEqual(response.status_code, 400)
