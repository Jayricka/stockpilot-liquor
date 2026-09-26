from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from billing.models import Plan, Subscription
from businesses.models import (
    Business,
    BusinessMembership,
)


class BusinessAPITestCase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            first_name="John",
            last_name="Owner",
        )

        self.manager = User.objects.create_user(
            email="manager@example.com",
            password="StrongPassword123",
            first_name="Jane",
            last_name="Manager",
        )

        self.staff = User.objects.create_user(
            email="staff@example.com",
            password="StrongPassword123",
            first_name="Peter",
            last_name="Staff",
        )

        self.business = Business.objects.create(
            name="Ricka Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        BusinessMembership.objects.create(
            user=self.owner,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.BUSINESS
        )

        self.subscription = Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=timezone.now(),
            trial_ends_at=(
                timezone.now()
                + timedelta(
                    days=self.plan.trial_days
                )
            ),
        )

        self.client.force_authenticate(
            user=self.owner
        )

    def url(self, name, **kwargs):
        return reverse(
            name,
            kwargs={
                "business_id": self.business.id,
                **kwargs,
            },
        )

    def test_business_list_returns_member_businesses(self):
        response = self.client.get(
            reverse("business-list-create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["name"],
            "Ricka Liquor Store",
        )

    def test_business_detail_returns_business(self):
        response = self.client.get(
            self.url("business-detail")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "Ricka Liquor Store",
        )

        self.assertEqual(
            response.data["role"],
            BusinessMembership.Role.OWNER,
        )

    def test_owner_can_update_business(self):
        response = self.client.patch(
            self.url("business-detail"),
            {
                "phone": "0799999999",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.business.refresh_from_db()

        self.assertEqual(
            self.business.phone,
            "0799999999",
        )

    def test_member_list_returns_active_members(self):
        BusinessMembership.objects.create(
            user=self.manager,
            business=self.business,
            role=BusinessMembership.Role.MANAGER,
            is_active=True,
        )

        response = self.client.get(
            self.url("business-member-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_owner_can_add_member(self):
        response = self.client.post(
            self.url("business-member-add"),
            {
                "email": self.staff.email,
                "role": BusinessMembership.Role.STAFF,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        membership = BusinessMembership.objects.get(
            user=self.staff,
            business=self.business,
        )

        self.assertEqual(
            membership.role,
            BusinessMembership.Role.STAFF,
        )

    def test_owner_can_change_member_role(self):
        BusinessMembership.objects.create(
            user=self.staff,
            business=self.business,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )

        response = self.client.patch(
            self.url(
                "business-member-role",
                user_id=self.staff.id,
            ),
            {
                "role": BusinessMembership.Role.MANAGER,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        membership = BusinessMembership.objects.get(
            user=self.staff,
            business=self.business,
        )

        self.assertEqual(
            membership.role,
            BusinessMembership.Role.MANAGER,
        )

    def test_owner_can_deactivate_member(self):
        BusinessMembership.objects.create(
            user=self.staff,
            business=self.business,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )

        response = self.client.delete(
            self.url(
                "business-member-deactivate",
                user_id=self.staff.id,
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        membership = BusinessMembership.objects.get(
            user=self.staff,
            business=self.business,
        )

        self.assertFalse(
            membership.is_active
        )

    def test_unauthenticated_business_list_is_rejected(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse("business-list-create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
