from django.urls import reverse
from rest_framework import status

from accounts.models import User
from billing.models import Plan, Subscription
from businesses.models import Business, BusinessMembership
from businesses.tests.base import BusinessOnboardingTestBase


class BusinessMembershipAPITestCase(BusinessOnboardingTestBase):
    def setUp(self):
        super().setUp()
        response = self.client.post(
            self.url,
            self.payload("business"),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.business = Business.objects.get(
            pk=response.data["business"]["id"]
        )
        self.subscription = Subscription.objects.get(
            business=self.business
        )
        self.members_url = reverse(
            "business-members",
            kwargs={"business_id": self.business.id},
        )

    def create_user(self, email):
        return User.objects.create_user(
            email=email,
            password="StrongPassword123",
        )

    def add_member(self, email, role="STAFF"):
        return self.client.post(
            self.members_url,
            {"email": email, "role": role},
            format="json",
        )

    def member_url(self, user):
        return reverse(
            "business-member-detail",
            kwargs={
                "business_id": self.business.id,
                "user_id": user.id,
            },
        )

    def test_owner_can_add_manager_and_staff(self):
        manager = self.create_user("manager@example.com")
        staff = self.create_user("staff@example.com")

        manager_response = self.add_member(manager.email, "MANAGER")
        staff_response = self.add_member(staff.email, "STAFF")

        self.assertEqual(manager_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(staff_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            BusinessMembership.objects.filter(
                business=self.business,
                is_active=True,
            ).count(),
            3,
        )

    def test_starter_plan_rejects_additional_member(self):
        self.subscription.plan = Plan.objects.get(
            code=Plan.Code.STARTER,
            is_active=True,
        )
        self.subscription.save(update_fields=["plan"])
        self.create_user("manager@example.com")

        response = self.add_member("manager@example.com", "MANAGER")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            BusinessMembership.objects.filter(
                business=self.business,
            ).count(),
            1,
        )

    def test_manager_can_add_staff_but_cannot_manage_managers(self):
        manager = self.create_user("manager@example.com")
        staff = self.create_user("staff@example.com")
        self.assertEqual(
            self.add_member(manager.email, "MANAGER").status_code,
            status.HTTP_201_CREATED,
        )

        self.client.force_authenticate(user=manager)
        add_staff_response = self.add_member(staff.email, "STAFF")
        change_manager_response = self.client.patch(
            self.member_url(manager),
            {"role": "STAFF"},
            format="json",
        )

        self.assertEqual(add_staff_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            change_manager_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_manager_cannot_promote_staff(self):
        manager = self.create_user("manager@example.com")
        staff = self.create_user("staff@example.com")
        self.assertEqual(
            self.add_member(manager.email, "MANAGER").status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            self.add_member(staff.email, "STAFF").status_code,
            status.HTTP_201_CREATED,
        )

        self.client.force_authenticate(user=manager)
        response = self.client.patch(
            self.member_url(staff),
            {"role": "MANAGER"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        staff_membership = BusinessMembership.objects.get(
            business=self.business,
            user=staff,
        )
        self.assertEqual(staff_membership.role, BusinessMembership.Role.STAFF)

    def test_duplicate_active_membership_is_rejected(self):
        staff = self.create_user("staff@example.com")
        self.assertEqual(
            self.add_member(staff.email).status_code,
            status.HTTP_201_CREATED,
        )

        response = self.add_member(staff.email)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            BusinessMembership.objects.filter(
                business=self.business,
                user=staff,
            ).count(),
            1,
        )

    def test_inactive_membership_is_reactivated_without_duplicate(self):
        staff = self.create_user("staff@example.com")
        membership = BusinessMembership.objects.create(
            business=self.business,
            user=staff,
            role=BusinessMembership.Role.STAFF,
            is_active=False,
        )

        response = self.add_member(staff.email)
        membership.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(membership.is_active)
        self.assertEqual(
            BusinessMembership.objects.filter(
                business=self.business,
                user=staff,
            ).count(),
            1,
        )

    def test_unknown_email_is_rejected(self):
        response = self.add_member("missing@example.com")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_cannot_deactivate_own_membership(self):
        response = self.client.delete(self.member_url(self.user))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        owner_membership = BusinessMembership.objects.get(
            business=self.business,
            user=self.user,
        )
        self.assertTrue(owner_membership.is_active)

    def test_expired_subscription_rejects_membership_changes(self):
        self.subscription.status = Subscription.Status.EXPIRED
        self.subscription.save(update_fields=["status"])
        self.create_user("staff@example.com")

        response = self.add_member("staff@example.com")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            BusinessMembership.objects.filter(
                business=self.business,
                user__email="staff@example.com",
            ).exists()
        )
