from django.db import migrations


def update_prices(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")

    prices = {
        "starter": 1499,
        "growth": 2499,
        "business": 3499,
    }

    for code, price in prices.items():
        Plan.objects.filter(
            code=code,
        ).update(
            price=price,
        )


def reverse_prices(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")

    prices = {
        "starter": 999,
        "growth": 1999,
        "business": 3999,
    }

    for code, price in prices.items():
        Plan.objects.filter(
            code=code,
        ).update(
            price=price,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0004_seed_plan_entitlements"),
    ]

    operations = [
        migrations.RunPython(
            update_prices,
            reverse_prices,
        ),
    ]
