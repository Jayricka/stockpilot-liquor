from billing.models import Plan, PlanEntitlement, Subscription
from billing.services.entitlements import EntitlementService

from .base import BillingAPITestBase


class EntitlementServiceTests(BillingAPITestBase):

    def setUp(self):
        super().setUp()

        self.starter = Plan.objects.get(
            code=Plan.Code.STARTER,
        )
        self.growth = Plan.objects.get(
            code=Plan.Code.GROWTH,
        )
        self.business_plan = Plan.objects.get(
            code=Plan.Code.BUSINESS,
        )

    def create_subscription(
        self,
        plan,
        status=Subscription.Status.ACTIVE,
    ):
        self.subscription.delete()

        return Subscription.objects.create(
            business=self.business,
            plan=plan,
            status=status,
        )

    def test_starter_has_core_features(self):
        self.create_subscription(self.starter)

        core_features = [
            PlanEntitlement.Feature.INVENTORY,
            PlanEntitlement.Feature.SALES,
            PlanEntitlement.Feature.PURCHASES,
            PlanEntitlement.Feature.SUPPLIERS,
            PlanEntitlement.Feature.REPORTS,
        ]

        for feature in core_features:
            with self.subTest(feature=feature):
                self.assertTrue(
                    EntitlementService.has_feature(
                        self.business,
                        feature,
                    )
                )

    def test_starter_does_not_have_deliveries(self):
        self.create_subscription(self.starter)

        self.assertFalse(
            EntitlementService.has_feature(
                self.business,
                PlanEntitlement.Feature.DELIVERIES,
            )
        )

    def test_growth_has_deliveries(self):
        self.create_subscription(self.growth)

        self.assertTrue(
            EntitlementService.has_feature(
                self.business,
                PlanEntitlement.Feature.DELIVERIES,
            )
        )

    def test_growth_does_not_have_advanced_reports(self):
        self.create_subscription(self.growth)

        self.assertFalse(
            EntitlementService.has_feature(
                self.business,
                PlanEntitlement.Feature.ADVANCED_REPORTS,
            )
        )

    def test_business_has_advanced_reports(self):
        self.create_subscription(
            self.business_plan,
        )

        self.assertTrue(
            EntitlementService.has_feature(
                self.business,
                PlanEntitlement.Feature.ADVANCED_REPORTS,
            )
        )

    def test_missing_subscription_denies_feature(self):
        self.subscription.delete()

        self.assertFalse(
            EntitlementService.has_feature(
                self.business,
                PlanEntitlement.Feature.INVENTORY,
            )
        )

    def test_expired_subscription_denies_feature(self):
        self.create_subscription(
            self.starter,
            Subscription.Status.EXPIRED,
        )

        self.assertFalse(
            EntitlementService.has_feature(
                self.business,
                PlanEntitlement.Feature.INVENTORY,
            )
        )

    def test_trialing_subscription_allows_feature(self):
        self.create_subscription(
            self.starter,
            Subscription.Status.TRIALING,
        )

        self.assertTrue(
            EntitlementService.has_feature(
                self.business,
                PlanEntitlement.Feature.INVENTORY,
            )
        )

    def test_require_feature_returns_true_when_allowed(self):
        self.create_subscription(self.starter)

        self.assertTrue(
            EntitlementService.require_feature(
                self.business,
                PlanEntitlement.Feature.SALES,
            )
        )

    def test_require_feature_raises_when_denied(self):
        self.create_subscription(self.starter)

        with self.assertRaises(PermissionError):
            EntitlementService.require_feature(
                self.business,
                PlanEntitlement.Feature.DELIVERIES,
            )
