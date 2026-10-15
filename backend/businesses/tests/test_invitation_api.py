from django.urls import reverse
from rest_framework import status

from accounts.models import User
from businesses.models import BusinessInvitation, BusinessMembership
from businesses.tests.base import BusinessOnboardingTestBase


class BusinessInvitationAPITestCase(BusinessOnboardingTestBase):
    def setUp(self):
        super().setUp()

        from businesses.models import Business
        from billing.models import Subscription

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
        self.invitations_url = reverse(
            "business-invitations",
            kwargs={"business_id": self.business.id},
        )

    def create_user(self, email):
        return User.objects.create_user(
            email=email,
            password="StrongPassword123",
        )

    def create_invitation(self, email, role="STAFF"):
        return self.client.post(
            self.invitations_url,
            {"email": email, "role": role},
            format="json",
        )

    def test_owner_can_create_invitation(self):
        response = self.create_invitation("staff@example.com")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["invitation"]["email"],
            "staff@example.com",
        )
        self.assertIn("token", response.data)
        self.assertTrue(
            BusinessInvitation.objects.filter(
                business=self.business,
                email="staff@example.com",
                status=BusinessInvitation.Status.PENDING,
            ).exists()
        )

    def test_invalid_email_is_rejected(self):
        response = self.create_invitation("not-an-email")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_pending_invitation_is_rejected(self):
        self.create_invitation("staff@example.com")

        response = self.create_invitation("staff@example.com")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_can_list_invitations_without_tokens(self):
        self.create_invitation("staff@example.com")

        response = self.client.get(self.invitations_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotIn("token", response.data[0])
        self.assertNotIn("token_hash", response.data[0])

    def test_owner_can_revoke_invitation(self):
        created = self.create_invitation("staff@example.com")
        invitation_id = created.data["invitation"]["id"]
        revoke_url = reverse(
            "business-invitation-detail",
            kwargs={
                "business_id": self.business.id,
                "invitation_id": invitation_id,
            },
        )

        response = self.client.delete(revoke_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        invitation = BusinessInvitation.objects.get(pk=invitation_id)
        self.assertEqual(
            invitation.status,
            BusinessInvitation.Status.REVOKED,
        )

    def test_user_without_business_membership_cannot_list_invitations(self):
        other_user = self.create_user("other@example.com")
        self.client.force_authenticate(user=other_user)

        response = self.client.get(self.invitations_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_cannot_create_invitation(self):
        self.client.force_authenticate(user=None)

        response = self.create_invitation("staff@example.com")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_accept_endpoint_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse("accept-business-invitation"),
            {"token": "example-token"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_expired_invitation_is_marked_expired_when_listed(self):
        from datetime import timedelta
        from django.utils import timezone

        response = self.create_invitation("staff@example.com")
        invitation = BusinessInvitation.objects.get(
            pk=response.data["invitation"]["id"]
        )
        invitation.expires_at = timezone.now() - timedelta(minutes=1)
        invitation.save(update_fields=["expires_at"])

        list_response = self.client.get(self.invitations_url)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        invitation.refresh_from_db()
        self.assertEqual(invitation.status, BusinessInvitation.Status.EXPIRED)

    def test_acceptance_rechecks_capacity(self):
        from rest_framework.exceptions import ValidationError
        from billing.models import Plan
        from businesses.services import BusinessInvitationService

        self.subscription.plan = Plan.objects.get(
            code=Plan.Code.BUSINESS,
            is_active=True,
        )
        self.subscription.save(update_fields=["plan"])

        created = self.create_invitation("staff@example.com")
        existing_staff = self.create_user("existing@example.com")
        BusinessMembership.objects.create(
            business=self.business,
            user=existing_staff,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )
        another_staff = self.create_user("another@example.com")
        BusinessMembership.objects.create(
            business=self.business,
            user=another_staff,
            role=BusinessMembership.Role.STAFF,
            is_active=True,
        )
        invited_user = self.create_user("staff@example.com")

        with self.assertRaises(ValidationError):
            BusinessInvitationService.accept_invitation(
                token=created.data["token"],
                actor=invited_user,
            )

        self.assertFalse(
            BusinessMembership.objects.filter(
                business=self.business,
                user=invited_user,
                is_active=True,
            ).exists()
        )
