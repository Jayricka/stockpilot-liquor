from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from businesses.models import Business, BusinessMembership


class BusinessAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="owner@test.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="Owner",
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="TestPassword123!",
            first_name="Other",
            last_name="Owner",
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def test_authenticated_user_can_create_business(self):
        response = self.client.post(
            "/api/businesses/",
            {
                "name": "Test Liquor Store",
                "business_type": "liquor_store",
                "phone": "0712345678",
                "email": "store@test.com",
                "address": "Kilimani, Nairobi",
                "license_number": "LIC-001",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        business = Business.objects.get(
            name="Test Liquor Store"
        )

        self.assertTrue(
            BusinessMembership.objects.filter(
                user=self.user,
                business=business,
                role=BusinessMembership.Role.OWNER,
                is_active=True,
            ).exists()
        )

    def test_user_can_only_see_their_businesses(self):
        own_business = Business.objects.create(
            name="My Liquor Store",
            business_type="liquor_store",
            phone="0711111111",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=own_business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0722222222",
        )

        BusinessMembership.objects.create(
            user=self.other_user,
            business=other_business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        response = self.client.get(
            "/api/businesses/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            own_business.id,
        )

    def test_user_cannot_create_duplicate_business_name(self):
        business = Business.objects.create(
            name="Ricka Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        response = self.client.post(
            "/api/businesses/",
            {
                "name": "  ricka liquor store  ",
                "business_type": "liquor_store",
                "phone": "0799999999",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["detail"],
            "You already have a business with this name.",
        )

        self.assertEqual(
            Business.objects.filter(
                memberships__user=self.user
            ).count(),
            1,
        )

    def test_different_users_can_have_same_business_name(self):
        existing_business = Business.objects.create(
            name="Town Liquor Store",
            business_type="liquor_store",
            phone="0711111111",
        )

        BusinessMembership.objects.create(
            user=self.other_user,
            business=existing_business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        response = self.client.post(
            "/api/businesses/",
            {
                "name": "Town Liquor Store",
                "business_type": "liquor_store",
                "phone": "0722222222",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            Business.objects.filter(
                name="Town Liquor Store"
            ).count(),
            2,
        )

    def test_inactive_membership_is_not_returned(self):
        business = Business.objects.create(
            name="Inactive Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=business,
            role=BusinessMembership.Role.OWNER,
            is_active=False,
        )

        response = self.client.get(
            "/api/businesses/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_unauthenticated_user_cannot_access_businesses(self):
        self.client.credentials()

        response = self.client.get(
            "/api/businesses/"
        )

        self.assertEqual(response.status_code, 401)
