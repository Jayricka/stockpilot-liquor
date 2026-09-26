from django.db import migrations


PLAN_ENTITLEMENTS = {
    "starter": {
        "max_users": 1,
        "max_owners": 1,
        "max_managers": 0,
        "max_staff": 0,
        "products": True,
        "inventory": True,
        "sales": True,
        "purchases": True,
        "suppliers": True,
        "deliveries": False,
        "reports": True,
        "advanced_reports": False,
        "business_analytics": False,
    },
    "growth": {
        "max_users": 3,
        "max_owners": 1,
        "max_managers": 2,
        "max_staff": 0,
        "products": True,
        "inventory": True,
        "sales": True,
        "purchases": True,
        "suppliers": True,
        "deliveries": True,
        "reports": True,
        "advanced_reports": True,
        "business_analytics": False,
    },
    "business": {
        "max_users": 5,
        "max_owners": 1,
        "max_managers": 2,
        "max_staff": 2,
        "products": True,
        "inventory": True,
        "sales": True,
        "purchases": True,
        "suppliers": True,
        "deliveries": True,
        "reports": True,
        "advanced_reports": True,
        "business_analytics": True,
    },
}


INTEGER_FEATURES = {
    "max_users",
    "max_owners",
    "max_managers",
    "max_staff",
}


def seed_entitlements(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")
    PlanEntitlement = apps.get_model(
        "billing",
        "PlanEntitlement",
    )

    for plan_code, entitlements in PLAN_ENTITLEMENTS.items():
        plan = Plan.objects.get(code=plan_code)

        for feature, value in entitlements.items():
            if feature in INTEGER_FEATURES:
                PlanEntitlement.objects.create(
                    plan=plan,
                    feature=feature,
                    value_type="INTEGER",
                    integer_value=value,
                )
            else:
                PlanEntitlement.objects.create(
                    plan=plan,
                    feature=feature,
                    value_type="BOOLEAN",
                    boolean_value=value,
                )


def remove_entitlements(apps, schema_editor):
    PlanEntitlement = apps.get_model(
        "billing",
        "PlanEntitlement",
    )

    PlanEntitlement.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0003_planentitlement"),
    ]

    operations = [
        migrations.RunPython(
            seed_entitlements,
            remove_entitlements,
        ),
    ]
