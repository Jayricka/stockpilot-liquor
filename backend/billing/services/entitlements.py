from billing.models import PlanEntitlement, Subscription


class EntitlementService:
    BOOLEAN_TRUE = "true"

    @staticmethod
    def get_subscription(business):
        try:
            return (
                Subscription.objects
                .select_related("plan")
                .get(business=business)
            )
        except Subscription.DoesNotExist:
            return None

    @staticmethod
    def get_value(plan, feature):
        return (
            PlanEntitlement.objects
            .filter(
                plan=plan,
                feature=feature,
            )
            .values_list("value", flat=True)
            .first()
        )

    @staticmethod
    def _has_operational_subscription(subscription):
        return (
            subscription is not None
            and subscription.status in {
                Subscription.Status.TRIALING,
                Subscription.Status.ACTIVE,
            }
        )

    @classmethod
    def has_feature(cls, business, feature):
        subscription = cls.get_subscription(business)

        if not cls._has_operational_subscription(
            subscription
        ):
            return False

        value = cls.get_value(
            subscription.plan,
            feature,
        )

        return (
            isinstance(value, str)
            and value.strip().lower() == cls.BOOLEAN_TRUE
        )

    @classmethod
    def get_limit(cls, business, feature):
        subscription = cls.get_subscription(business)

        if not cls._has_operational_subscription(
            subscription
        ):
            return None

        value = cls.get_value(
            subscription.plan,
            feature,
        )

        if value is None:
            return None

        try:
            limit = int(value)
        except (TypeError, ValueError):
            return None

        if limit < 0:
            return None

        return limit

    @classmethod
    def get_all(cls, business):
        subscription = cls.get_subscription(business)

        if not cls._has_operational_subscription(
            subscription
        ):
            return {}

        rows = (
            PlanEntitlement.objects
            .filter(plan=subscription.plan)
            .values_list("feature", "value")
        )

        result = {}

        for feature, value in rows:
            if feature.startswith("max_"):
                try:
                    result[feature] = int(value)
                except (TypeError, ValueError):
                    result[feature] = None
            else:
                result[feature] = (
                    value.strip().lower()
                    == cls.BOOLEAN_TRUE
                )

        return result

    @classmethod
    def require_feature(cls, business, feature):
        if not cls.has_feature(business, feature):
            raise PermissionError(
                f"The current plan does not include "
                f"the '{feature}' feature."
            )

        return True
