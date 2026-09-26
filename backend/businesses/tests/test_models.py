from django.test import TestCase

from accounts.models import User
from businesses.models import (
    Business,
    BusinessMembership,
)


class BusinessModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            first_name="John",
            last_name="Owner",
        )

        self.business = Business.objects.create(
            name="Ricka Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

    def test_business_string_representation(self):
        self.assertEqual(
            str(self.business),
            "Ricka Liquor Store",
        )

    def test_business_defaults(self):
        self.assertTrue(
            self.business.is_active
        )

        self.assertEqual(
            self.business.business_type,
            "liquor_store",
        )

    def test_membership_string_representation(self):
        membership = BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
        )

        self.assertEqual(
            str(membership),
            "owner@example.com - Ricka Liquor Store",
        )

    def test_membership_defaults_to_staff(self):
        membership = BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
        )

        self.assertEqual(
            membership.role,
            BusinessMembership.Role.STAFF,
        )

        self.assertTrue(
            membership.is_active
        )

    def test_membership_role_choices(self):
        self.assertEqual(
            BusinessMembership.Role.OWNER,
            "OWNER",
        )

        self.assertEqual(
            BusinessMembership.Role.MANAGER,
            "MANAGER",
        )

        self.assertEqual(
            BusinessMembership.Role.STAFF,
            "STAFF",
        )

    def test_user_cannot_have_duplicate_business_membership(
        self,
    ):
        BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
        )

        with self.assertRaises(Exception):
            BusinessMembership.objects.create(
                user=self.user,
                business=self.business,
                role=BusinessMembership.Role.STAFF,
            )
