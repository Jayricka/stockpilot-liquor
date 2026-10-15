from datetime import timedelta
from hashlib import sha256

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from businesses.models import (
    BusinessInvitation,
    BusinessMembership,
)
from businesses.services import BusinessInvitationService
from businesses.tests.base import BusinessOnboardingTestBase


class BusinessInvitationServiceTestCase(
    BusinessOnboardingTestBase
):
    def setUp(self):
        super().setUp()

        response = self.client.post(
            self.url,
            self.payload("business"),
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        from businesses.models import Business

        self.business = Business.objects.get(
            pk=response.data["business"]["id"]
        )

    def create_user(self, email):
        from accounts.models import User

        return User.objects.create_user(
            email=email,
            password="StrongPassword123",
        )

    def create_invitation(self, email="staff@example.com"):
        return BusinessInvitationService.create_invitation(
            business_id=self.business.id,
            actor=self.user,
            email=email,
            role=BusinessInvitation.Role.STAFF,
        )

    def test_owner_can_create_invitation(self):
        invitation, raw_token = self.create_invitation()

        self.assertEqual(
            invitation.email,
            "staff@example.com",
        )
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.PENDING,
        )
        self.assertEqual(invitation.invited_by, self.user)
        self.assertTrue(raw_token)
        self.assertNotEqual(
            invitation.token_hash,
            raw_token,
        )
        self.assertEqual(
            invitation.token_hash,
            sha256(raw_token.encode()).hexdigest(),
        )

    def test_invitation_expires_after_seven_days(self):
        before = timezone.now()

        invitation, _raw_token = self.create_invitation()

        expected_expiry = before + timedelta(days=7)
        difference = abs(
            (invitation.expires_at - expected_expiry).total_seconds()
        )

        self.assertLess(difference, 5)

    def test_duplicate_pending_invitation_is_rejected(self):
        self.create_invitation()

        with self.assertRaises(ValidationError):
            self.create_invitation("STAFF@example.com")

    def test_owner_cannot_invite_an_existing_active_member(self):
        member = self.create_user("existing@example.com")
        BusinessMembership.objects.create(
            business=self.business,
            user=member,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            self.create_invitation(member.email)

    def test_manager_cannot_invite_another_manager(self):
        manager = self.create_user("manager@example.com")
        BusinessMembership.objects.create(
            business=self.business,
            user=manager,
            role=BusinessMembership.Role.MANAGER,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            BusinessInvitationService.create_invitation(
                business_id=self.business.id,
                actor=manager,
                email="another@example.com",
                role=BusinessInvitation.Role.MANAGER,
            )

    def test_staff_cannot_invite_members(self):
        staff = self.create_user("staff@example.com")
        BusinessMembership.objects.create(
            business=self.business,
            user=staff,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            BusinessInvitationService.create_invitation(
                business_id=self.business.id,
                actor=staff,
                email="another@example.com",
                role=BusinessInvitation.Role.STAFF,
            )

    def test_owner_role_cannot_be_invited(self):
        with self.assertRaises(ValidationError):
            BusinessInvitationService.create_invitation(
                business_id=self.business.id,
                actor=self.user,
                email="another@example.com",
                role="OWNER",
            )

    def test_expired_subscription_rejects_invitation(self):
        from billing.models import Subscription

        subscription = Subscription.objects.get(
            business=self.business
        )
        subscription.status = Subscription.Status.EXPIRED
        subscription.save(update_fields=["status"])

        with self.assertRaises(ValidationError):
            self.create_invitation()

        self.assertFalse(
            BusinessInvitation.objects.filter(
                business=self.business
            ).exists()
        )

    def test_staff_invitation_capacity_is_enforced(self):
        self.create_invitation("staff1@example.com")
        self.create_invitation("staff2@example.com")

        with self.assertRaises(ValidationError):
            self.create_invitation("staff3@example.com")

        self.assertEqual(
            BusinessInvitation.objects.filter(
                business=self.business,
                status=BusinessInvitation.Status.PENDING,
            ).count(),
            2,
        )

    def test_owner_can_revoke_pending_invitation(self):
        invitation, _raw_token = self.create_invitation()

        revoked = BusinessInvitationService.revoke_invitation(
            business_id=self.business.id,
            actor=self.user,
            invitation_id=invitation.id,
        )

        self.assertEqual(
            revoked.status,
            BusinessInvitation.Status.REVOKED,
        )

    def test_manager_can_revoke_staff_invitation(self):
        manager = self.create_user("manager-revoke@example.com")
        BusinessMembership.objects.create(
            business=self.business,
            user=manager,
            role=BusinessMembership.Role.MANAGER,
            is_active=True,
        )
        invitation, _raw_token = self.create_invitation()

        revoked = BusinessInvitationService.revoke_invitation(
            business_id=self.business.id,
            actor=manager,
            invitation_id=invitation.id,
        )

        self.assertEqual(
            revoked.status,
            BusinessInvitation.Status.REVOKED,
        )

    def test_staff_cannot_revoke_invitation(self):
        staff = self.create_user("staff-revoke@example.com")
        BusinessMembership.objects.create(
            business=self.business,
            user=staff,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )
        invitation, _raw_token = self.create_invitation()

        with self.assertRaises(ValidationError):
            BusinessInvitationService.revoke_invitation(
                business_id=self.business.id,
                actor=staff,
                invitation_id=invitation.id,
            )

        invitation.refresh_from_db()
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.PENDING,
        )

    def accept_invitation(self, token, user):
        return BusinessInvitationService.accept_invitation(
            token=token,
            actor=user,
        )

    def test_invited_user_can_accept_invitation(self):
        invitation, token = self.create_invitation()
        user = self.create_user("staff@example.com")

        membership = self.accept_invitation(token, user)

        invitation.refresh_from_db()
        self.assertEqual(membership.business, self.business)
        self.assertEqual(membership.user, user)
        self.assertEqual(
            membership.role,
            BusinessMembership.Role.STAFF,
        )
        self.assertTrue(membership.is_active)
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.ACCEPTED,
        )
        self.assertEqual(invitation.accepted_by, user)
        self.assertIsNotNone(invitation.accepted_at)

    def test_invalid_token_is_rejected(self):
        user = self.create_user("staff@example.com")

        with self.assertRaises(ValidationError):
            self.accept_invitation("invalid-token", user)

    def test_email_mismatch_is_rejected(self):
        invitation, token = self.create_invitation()
        user = self.create_user("other@example.com")

        with self.assertRaises(ValidationError):
            self.accept_invitation(token, user)

        invitation.refresh_from_db()
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.PENDING,
        )

    def test_expired_invitation_cannot_be_accepted(self):
        invitation, token = self.create_invitation()
        user = self.create_user("staff@example.com")

        invitation.expires_at = timezone.now() - timedelta(minutes=1)
        invitation.save(update_fields=["expires_at"])

        with self.assertRaises(ValidationError):
            self.accept_invitation(token, user)

        invitation.refresh_from_db()
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.EXPIRED,
        )
        self.assertFalse(
            BusinessMembership.objects.filter(
                business=self.business,
                user=user,
            ).exists()
        )

    def test_revoked_invitation_cannot_be_accepted(self):
        invitation, token = self.create_invitation()
        user = self.create_user("staff@example.com")

        BusinessInvitationService.revoke_invitation(
            business_id=self.business.id,
            actor=self.user,
            invitation_id=invitation.id,
        )

        with self.assertRaises(ValidationError):
            self.accept_invitation(token, user)

        self.assertFalse(
            BusinessMembership.objects.filter(
                business=self.business,
                user=user,
            ).exists()
        )

    def test_active_member_cannot_accept_invitation_again(self):
        invitation, token = self.create_invitation()
        user = self.create_user("staff@example.com")

        BusinessMembership.objects.create(
            business=self.business,
            user=user,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            self.accept_invitation(token, user)

        invitation.refresh_from_db()
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.PENDING,
        )

    def test_inactive_membership_is_reactivated_on_acceptance(self):
        invitation, token = self.create_invitation()
        user = self.create_user("staff@example.com")
        existing = BusinessMembership.objects.create(
            business=self.business,
            user=user,
            role=BusinessMembership.Role.MANAGER,
            is_active=False,
        )

        membership = self.accept_invitation(token, user)

        existing.refresh_from_db()
        invitation.refresh_from_db()

        self.assertEqual(membership.pk, existing.pk)
        self.assertTrue(existing.is_active)
        self.assertEqual(
            existing.role,
            BusinessMembership.Role.STAFF,
        )
        self.assertEqual(
            BusinessMembership.objects.filter(
                business=self.business,
                user=user,
            ).count(),
            1,
        )
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.ACCEPTED,
        )

    def test_acceptance_rejects_expired_subscription(self):
        invitation, token = self.create_invitation()
        user = self.create_user("staff@example.com")

        from billing.models import Subscription

        subscription = Subscription.objects.get(
            business=self.business
        )
        subscription.status = Subscription.Status.EXPIRED
        subscription.save(update_fields=["status"])

        with self.assertRaises(ValidationError):
            self.accept_invitation(token, user)

        invitation.refresh_from_db()
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.PENDING,
        )
        self.assertFalse(
            BusinessMembership.objects.filter(
                business=self.business,
                user=user,
            ).exists()
        )

    def test_accepting_invitation_twice_is_rejected(self):
        invitation, token = self.create_invitation()
        user = self.create_user("staff@example.com")

        self.accept_invitation(token, user)

        with self.assertRaises(ValidationError):
            self.accept_invitation(token, user)

        invitation.refresh_from_db()
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.ACCEPTED,
        )
        self.assertEqual(
            BusinessMembership.objects.filter(
                business=self.business,
                user=user,
            ).count(),
            1,
        )
