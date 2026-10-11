from django.db import migrations


PLAN_ENTITLEMENTS = {
    "starter": {
        "products": "true",
        "inventory": "true",
        "sales": "true",
        "purchases": "true",
        "suppliers": "true",
        "deliveries": "false",
        "reports": "true",
        "advanced_reports": "false",
        "business_analytics": "false",
        "max_users": "1",
        "max_owners": "1",
        "max_managers": "0",
        "max_staff": "0",
    },
    "growth": {
        "products": "true",
        "inventory": "true",
        "sales": "true",
        "purchases": "true",
        "suppliers": "true",
        "deliveries": "true",
        "reports": "true",
        "advanced_reports": "true",
        "business_analytics": "false",
        "max_users": "3",
        "max_owners": "1",
        "max_managers": "2",
        "max_staff": "0",
    },
    "business": {
        "products": "true",
        "inventory": "true",
        "sales": "true",
        "purchases": "true",
        "suppliers": "true",
        "deliveries": "true",
        "reports": "true",
        "advanced_reports": "true",
        "business_analytics": "true",
        "max_users": "5",
        "max_owners": "1",
        "max_managers": "2",
        "max_staff": "2",
    },
}


def configure_plan_entitlements(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")
    PlanEntitlement = apps.get_model("billing", "PlanEntitlement")
    database = schema_editor.connection.alias

    for plan_code, entitlements in PLAN_ENTITLEMENTS.items():
        plan = (
            Plan.objects.using(database)
            .filter(code=plan_code)
            .first()
        )

        if plan is None:
            raise RuntimeError(
                f"Cannot configure entitlements: plan '{plan_code}' "
                "does not exist."
            )

        for feature, value in entitlements.items():
            PlanEntitlement.objects.using(database).update_or_create(
                plan=plan,
                feature=feature,
                defaults={"value": value},
            )


class Migration(migrations.Migration):
    dependencies = [
        ("billing", "0007_configure_plan_entitlements_v2"),
    ]

    operations = [
        migrations.RunPython(
            configure_plan_entitlements,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
