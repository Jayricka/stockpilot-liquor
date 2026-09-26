from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from billing.models import Plan, Subscription
from businesses.models import (
    Business,
    BusinessMembership,
)
from businesses.services.businesses import (
    BusinessOnboardingService,
    BusinessService,
)
from businesses.services.memberships import (
    BusinessMembershipService,
)


class BusinessServiceTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            first_name="John",
            last_name="Owner",
        )

    def business_data(self, name="Ricka Liquor Store"):
        return {
            "name": name,
            "business_type": "liquor_store",
            "phone": "0712345678",
            "email": "store@example.com",
            "address": "Nairobi",
            "license_number": "LIC-12345",
        }

    def test_create_business_creates_owner_membership(self):
        business = BusinessService.create_business(
            user=self.user,
            validated_data=self.business_data(),
        )

        self.assertEqual(
            business.name,
            "Ricka Liquor Store",
        )

        membership = BusinessMembership.objects.get(
            user=self.user,
            business=business,
        )

        self.assertEqual(
            membership.role,
            BusinessMembership.Role.OWNER,
        )

        self.assertTrue(
            membership.is_active
        )

    def test_create_business_strips_business_name(self):
        business = BusinessService.create_business(
            user=self.user,
            validated_data=self.business_data(
                "  Ricka Liquor Store  "
            ),
        )

        self.assertEqual(
            business.name,
            "Ricka Liquor Store",
        )

    def test_create_business_rejects_duplicate_name_for_user(
        self,
    ):
        BusinessService.create_business(
            user=self.user,
            validated_data=self.business_data(),
        )

        with self.assertRaisesMessage(
            ValueError,
            "You already have a business with this name.",
        ):
            BusinessService.create_business(
                user=self.user,
                validated_data=self.business_data(),
            )


class BusinessOnboardingServiceTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            first_name="John",
            last_name="Owner",
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.GROWTH
        )

    def business_data(self):
        return {
            "name": "Ricka Liquor Store",
            "business_type": "liquor_store",
            "phone": "0712345678",
            "email": "store@example.com",
            "address": "Nairobi",
            "license_number": "LIC-12345",
            "plan": self.plan,
        }

    def test_onboard_creates_business_and_subscription(self):
        business, subscription = (
            BusinessOnboardingService.onboard(
                user=self.user,
                validated_data=self.business_data(),
            )
        )

        self.assertEqual(
            business.name,
            "Ricka Liquor Store",
        )

        self.assertEqual(
            subscription.business,
            business,
        )

        self.assertEqual(
            subscription.plan,
            self.plan,
        )

        self.assertEqual(
            subscription.status,
            Subscription.Status.TRIALING,
        )

    def test_onboard_creates_trial_for_plan_duration(self):
        business, subscription = (
            BusinessOnboardingService.onboard(
                user=self.user,
                validated_data=self.business_data(),
            )
        )

        expected_end = (
            subscription.trial_started_at
            + timedelta(
                days=self.plan.trial_days
            )
        )

        difference = abs(
            (
                subscription.trial_ends_at
                - expected_end
            ).total_seconds()
        )

        self.assertLess(
            difference,
            2,
        )


class BusinessMembershipServiceTestCase(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
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

    def create_user(self, email):
        return User.objects.create_user(
            email=email,
            password="StrongPassword123",
        )

    def test_add_member_creates_membership(self):
        user = self.create_user(
            "manager@example.com"
        )

        membership = (
            BusinessMembershipService.add_member(
                business=self.business,
                email=user.email,
                role=BusinessMembership.Role.MANAGER,
            )
        )

        self.assertEqual(
            membership.user,
            user,
        )

        self.assertEqual(
            membership.role,
            BusinessMembership.Role.MANAGER,
        )

        self.assertTrue(
            membership.is_active
        )

    def test_add_member_is_case_insensitive(self):
        user = self.create_user(
            "manager@example.com"
        )

        membership = (
            BusinessMembershipService.add_member(
                business=self.business,
                email="MANAGER@EXAMPLE.COM",
                role=BusinessMembership.Role.MANAGER,
            )
        )

        self.assertEqual(
            membership.user,
            user,
        )

    def test_add_member_rejects_unregistered_user(self):
        with self.assertRaisesMessage(
            ValueError,
            "No registered user exists with this email.",
        ):
            BusinessMembershipService.add_member(
                business=self.business,
                email="unknown@example.com",
                role=BusinessMembership.Role.MANAGER,
            )

    def test_add_member_rejects_duplicate_active_member(self):
        user = self.create_user(
            "manager@example.com"
        )

        BusinessMembershipService.add_member(
            business=self.business,
            email=user.email,
            role=BusinessMembership.Role.MANAGER,
        )

        with self.assertRaisesMessage(
            ValueError,
            "This user is already an active member.",
        ):
            BusinessMembershipService.add_member(
                business=self.business,
                email=user.email,
                role=BusinessMembership.Role.MANAGER,
            )

    def test_add_member_reactivates_inactive_membership(self):
        user = self.create_user(
            "staff@example.com"
        )

        membership = BusinessMembership.objects.create(
            user=user,
            business=self.business,
            role=BusinessMembership.Role.STAFF,
            is_active=False,
        )

        result = (
            BusinessMembershipService.add_member(
                business=self.business,
                email=user.email,
                role=BusinessMembership.Role.MANAGER,
            )
        )

        membership.refresh_from_db()

        self.assertEqual(
            result.id,
            membership.id,
        )

        self.assertEqual(
            membership.role,
            BusinessMembership.Role.MANAGER,
        )

        self.assertTrue(
            membership.is_active
        )

    def test_manager_limit_is_enforced(self):
        for index in range(2):
            user = self.create_user(
                f"manager{index}@example.com"
            )

            BusinessMembershipService.add_member(
                business=self.business,
                email=user.email,
                role=BusinessMembership.Role.MANAGER,
            )

        user = self.create_user(
            "manager3@example.com"
        )

        with self.assertRaisesMessage(
            ValueError,
            "up to 2 manager member(s)",
        ):
            BusinessMembershipService.add_member(
                business=self.business,
                email=user.email,
                role=BusinessMembership.Role.MANAGER,
            )

    def test_staff_limit_is_enforced(self):
        for index in range(2):
            user = self.create_user(
                f"staff{index}@example.com"
            )

            BusinessMembershipService.add_member(
                business=self.business,
                email=user.email,
                role=BusinessMembership.Role.STAFF,
            )

        user = self.create_user(
            "staff3@example.com"
        )

        with self.assertRaisesMessage(
            ValueError,
            "up to 2 staff member(s)",
        ):
            BusinessMembershipService.add_member(
                business=self.business,
                email=user.email,
                role=BusinessMembership.Role.STAFF,
            )

    def test_deactivate_member(self):
        user = self.create_user(
            "staff@example.com"
        )

        membership = BusinessMembership.objects.create(
            user=user,
            business=self.business,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )

        BusinessMembershipService.deactivate_member(
            business=self.business,
            user_id=user.id,
        )

        membership.refresh_from_db()

        self.assertFalse(
            membership.is_active
        )

    def test_owner_cannot_be_deactivated(self):
        with self.assertRaisesMessage(
            ValueError,
            "The business owner cannot be removed.",
        ):
            BusinessMembershipService.deactivate_member(
                business=self.business,
                user_id=self.owner.id,
            )

    def test_change_member_role(self):
        user = self.create_user(
            "staff@example.com"
        )

        BusinessMembership.objects.create(
            user=user,
            business=self.business,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )

        membership = (
            BusinessMembershipService.change_role(
                business=self.business,
                user_id=user.id,
                role=BusinessMembership.Role.MANAGER,
            )
        )

        self.assertEqual(
            membership.role,
            BusinessMembership.Role.MANAGER,
        )

    def test_owner_role_cannot_be_changed(self):
        with self.assertRaisesMessage(
            ValueError,
            "The business owner role cannot be changed.",
        ):
            BusinessMembershipService.change_role(
                business=self.business,
                user_id=self.owner.id,
                role=BusinessMembership.Role.MANAGER,
            )

    def test_expired_subscription_blocks_membership_changes(
        self,
    ):
        self.subscription.trial_ends_at = (
            timezone.now() - timedelta(days=1)
        )
        self.subscription.save(
            update_fields=["trial_ends_at"]
        )

        user = self.create_user(
            "manager@example.com"
        )

        with self.assertRaisesMessage(
            ValueError,
            "This subscription is not active.",
        ):
            BusinessMembershipService.add_member(
                business=self.business,
                email=user.email,
                role=BusinessMembership.Role.MANAGER,
            )
