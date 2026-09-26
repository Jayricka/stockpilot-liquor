from billing.models import PlanEntitlement


class PlanEntitlementService:

    @staticmethod
    def get_entitlement(plan, feature):
        try:
            return PlanEntitlement.objects.get(
                plan=plan,
                feature=feature,
            )
        except PlanEntitlement.DoesNotExist:
            return None

    @classmethod
    def has_feature(cls, plan, feature):
        entitlement = cls.get_entitlement(
            plan,
            feature,
        )

        if entitlement is None:
            return False

        if (
            entitlement.value_type
            != PlanEntitlement.ValueType.BOOLEAN
        ):
            return False

        return entitlement.boolean_value is True

    @classmethod
    def get_limit(cls, plan, feature):
        entitlement = cls.get_entitlement(
            plan,
            feature,
        )

        if entitlement is None:
            return None

        if (
            entitlement.value_type
            != PlanEntitlement.ValueType.INTEGER
        ):
            return None

        return entitlement.integer_value

    @classmethod
    def get_all(cls, plan):
        entitlements = PlanEntitlement.objects.filter(
            plan=plan,
        )

        result = {}

        for entitlement in entitlements:
            if (
                entitlement.value_type
                == PlanEntitlement.ValueType.BOOLEAN
            ):
                result[entitlement.feature] = (
                    entitlement.boolean_value
                )
            else:
                result[entitlement.feature] = (
                    entitlement.integer_value
                )

        return result
