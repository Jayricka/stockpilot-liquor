from datetime import timedelta

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from businesses.models import (
    Business,
    BusinessInvitation,
    BusinessMembership,
)


class BusinessInvitationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
        )

        self.business = Business.objects.create(
            name="Ricka Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        BusinessMembership.objects.create(
            business=self.business,
            user=self.user,
            role=BusinessMembership.Role.OWNER,
        )

    def create_invitation(self, **overrides):
        data = {
            "business": self.business,
            "email": "staff@example.com",
            "role": BusinessInvitation.Role.STAFF,
            "token_hash": "a" * 64,
            "invited_by": self.user,
            "expires_at": timezone.now() + timedelta(days=7),
        }
        data.update(overrides)
        return BusinessInvitation.objects.create(**data)

    def test_invitation_normalizes_email(self):
        invitation = self.create_invitation(
            email="  Staff@Example.COM  ",
        )

        self.assertEqual(
            invitation.email,
            "staff@example.com",
        )

    def test_invitation_defaults_to_pending(self):
        invitation = self.create_invitation()

        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.PENDING,
        )

    def test_invitation_rejects_duplicate_pending_email(self):
        self.create_invitation()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_invitation(
                    token_hash="b" * 64,
                    email="STAFF@example.com",
                )

    def test_non_pending_invitation_allows_new_pending_invitation(
        self,
    ):
        invitation = self.create_invitation()
        invitation.status = BusinessInvitation.Status.REVOKED
        invitation.save(update_fields=["status"])

        replacement = self.create_invitation(
            token_hash="b" * 64,
        )

        self.assertEqual(
            replacement.status,
            BusinessInvitation.Status.PENDING,
        )

    def test_token_hash_must_be_unique(self):
        self.create_invitation()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_invitation(
                    email="another@example.com",
                )

    def test_invitation_roles_exclude_owner(self):
        allowed_roles = {
            value
            for value, _label
            in BusinessInvitation.Role.choices
        }

        self.assertEqual(
            allowed_roles,
            {"MANAGER", "STAFF"},
        )

    def test_invitation_records_expiry_and_inviter(self):
        expires_at = timezone.now() + timedelta(days=3)
        invitation = self.create_invitation(
            expires_at=expires_at,
        )

        self.assertEqual(invitation.invited_by, self.user)
        self.assertEqual(invitation.expires_at, expires_at)
        self.assertIsNone(invitation.accepted_at)
        self.assertIsNone(invitation.accepted_by)
