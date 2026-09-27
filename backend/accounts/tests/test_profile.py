from .base import AccountsTestBase


class ProfileAPITests(AccountsTestBase):
    def authenticate(self):
        self.client.force_authenticate(
            user=self.user
        )

    def test_authenticated_user_can_view_profile(self):
        self.authenticate()

        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["id"],
            self.user.id,
        )
        self.assertEqual(
            response.data["email"],
            self.user.email,
        )
        self.assertEqual(
            response.data["first_name"],
            "Test",
        )
        self.assertEqual(
            response.data["last_name"],
            "User",
        )
        self.assertEqual(
            response.data["full_name"],
            "Test User",
        )

    def test_user_can_update_profile(self):
        self.authenticate()

        response = self.client.patch(
            self.me_url,
            {
                "first_name": "Updated",
                "last_name": "Name",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["first_name"],
            "Updated",
        )
        self.assertEqual(
            response.data["last_name"],
            "Name",
        )
        self.assertEqual(
            response.data["full_name"],
            "Updated Name",
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.first_name,
            "Updated",
        )
        self.assertEqual(
            self.user.last_name,
            "Name",
        )

    def test_user_can_partially_update_profile(self):
        self.authenticate()

        response = self.client.patch(
            self.me_url,
            {"first_name": "Updated"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["first_name"],
            "Updated",
        )
        self.assertEqual(
            response.data["last_name"],
            "User",
        )

    def test_profile_email_is_read_only(self):
        self.authenticate()

        response = self.client.patch(
            self.me_url,
            {"email": "changed@example.com"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["email"],
            self.user.email,
        )
