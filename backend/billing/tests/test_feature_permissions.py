from django.test import TestCase

from billing.models import Plan, PlanEntitlement, Subscription
from billing.permissions import HasFeatureAccess

from .base import BillingPermissionTestBase


class FeaturePermissionTests(
    BillingPermissionTestBase,
    TestCase,
):

    def setUp(self):
        super().setUp()

        self.permission = HasFeatureAccess()

        from rest_framework.views import APIView

        self.view = APIView()
        self.view.kwargs = {
            "business_id": self.business.id,
        }

        self.starter = Plan.objects.get(
            code=Plan.Code.STARTER,
        )
        self.growth = Plan.objects.get(
            code=Plan.Code.GROWTH,
        )
        self.business_plan = Plan.objects.get(
            code=Plan.Code.BUSINESS,
        )

    def set_feature(self, feature):
        self.view.required_feature = feature

    def test_starter_allows_inventory(self):
        self.create_subscription(
            status=Subscription.Status.ACTIVE,
        )

        self.set_feature(
            PlanEntitlement.Feature.INVENTORY,
        )

        request = self.get_request()

        self.assertTrue(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_starter_denies_deliveries(self):
        self.create_subscription(
            status=Subscription.Status.ACTIVE,
        )

        self.set_feature(
            PlanEntitlement.Feature.DELIVERIES,
        )

        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_growth_allows_deliveries(self):
        self.create_subscription(
            status=Subscription.Status.ACTIVE,
        ).delete()

        Subscription.objects.create(
            business=self.business,
            plan=self.growth,
            status=Subscription.Status.ACTIVE,
        )

        self.set_feature(
            PlanEntitlement.Feature.DELIVERIES,
        )

        request = self.get_request()

        self.assertTrue(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_growth_denies_advanced_reports(self):
        self.create_subscription(
            status=Subscription.Status.ACTIVE,
        ).delete()

        Subscription.objects.create(
            business=self.business,
            plan=self.growth,
            status=Subscription.Status.ACTIVE,
        )

        self.set_feature(
            PlanEntitlement.Feature.ADVANCED_REPORTS,
        )

        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_business_allows_advanced_reports(self):
        self.create_subscription(
            status=Subscription.Status.ACTIVE,
        ).delete()

        Subscription.objects.create(
            business=self.business,
            plan=self.business_plan,
            status=Subscription.Status.ACTIVE,
        )

        self.set_feature(
            PlanEntitlement.Feature.ADVANCED_REPORTS,
        )

        request = self.get_request()

        self.assertTrue(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_expired_subscription_denies_feature(self):
        self.create_subscription(
            status=Subscription.Status.EXPIRED,
        )

        self.set_feature(
            PlanEntitlement.Feature.INVENTORY,
        )

        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_missing_subscription_denies_feature(self):
        self.create_subscription(
            status=Subscription.Status.ACTIVE,
        ).delete()

        self.set_feature(
            PlanEntitlement.Feature.INVENTORY,
        )

        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )
