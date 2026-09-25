from django.db import migrations


def create_plans(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")

    Plan.objects.bulk_create(
        [
            Plan(
                code="starter",
                name="Starter",
                price=999,
                currency="KES",
                trial_days=7,
            ),
            Plan(
                code="growth",
                name="Growth",
                price=1999,
                currency="KES",
                trial_days=7,
            ),
            Plan(
                code="business",
                name="Business",
                price=3999,
                currency="KES",
                trial_days=7,
            ),
        ]
    )


def remove_plans(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")
    Plan.objects.filter(
        code__in=[
            "starter",
            "growth",
            "business",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_plans,
            remove_plans,
        ),
    ]
