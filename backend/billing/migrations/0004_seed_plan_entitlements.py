from django.db import migrations


def seed_entitlements(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")
    PlanEntitlement = apps.get_model(
        "billing",
        "PlanEntitlement",
    )

    feature_matrix = {
        "starter": {
            "inventory",
            "sales",
            "purchases",
            "suppliers",
            "reports",
        },
        "growth": {
            "inventory",
            "sales",
            "purchases",
            "suppliers",
            "deliveries",
            "reports",
        },
        "business": {
            "inventory",
            "sales",
            "purchases",
            "suppliers",
            "deliveries",
            "reports",
            "advanced_reports",
        },
    }

    for plan_code, features in feature_matrix.items():
        try:
            plan = Plan.objects.get(code=plan_code)
        except Plan.DoesNotExist:
            continue

        for feature in features:
            PlanEntitlement.objects.update_or_create(
                plan=plan,
                feature=feature,
                defaults={"value": "true"},
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
