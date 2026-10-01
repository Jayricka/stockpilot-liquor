from billing.models import PlanEntitlement, Subscription


class EntitlementService:
    @staticmethod
    def has_feature(business, feature):
        try:
            subscription = (
                Subscription.objects
                .select_related("plan")
                .get(business=business)
            )
        except Subscription.DoesNotExist:
            return False

        if subscription.status not in {
            Subscription.Status.TRIALING,
            Subscription.Status.ACTIVE,
        }:
            return False

        entitlement = (
            PlanEntitlement.objects
            .filter(
                plan=subscription.plan,
                feature=feature,
                value="true",
            )
            .exists()
        )

        return entitlement

    @staticmethod
    def require_feature(business, feature):
        if not EntitlementService.has_feature(
            business,
            feature,
        ):
            raise PermissionError(
                f"The current plan does not include "
                f"the '{feature}' feature."
            )

        return True
