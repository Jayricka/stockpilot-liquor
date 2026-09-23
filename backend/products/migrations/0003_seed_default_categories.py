from django.db import migrations


CATEGORIES = {
    "ALCOHOLIC_DRINKS": [
        "Gin",
        "Vodka",
        "Whisky",
        "Brandy",
        "Rum",
        "Tequila",
        "Wine",
        "Beer",
        "Cider",
        "Champagne",
        "Liqueurs",
        "Cocktails / RTD",
    ],
    "SODA_AND_DRINKS": [
        "Soda",
        "Energy Drinks",
        "Juice",
        "Water",
        "Tonic & Mixers",
        "Sports Drinks",
        "Iced Tea",
    ],
    "CIGARETTES_AND_TOBACCO": [
        "Cigarettes",
        "Cigars",
        "Rolling Tobacco",
        "Shisha Tobacco",
        "Matches & Lighters",
    ],
    "OTHER": [
        "Snacks",
        "Ice",
        "Glassware",
        "Bar Accessories",
        "Other",
    ],
}


def seed_categories(apps, schema_editor):
    Business = apps.get_model("businesses", "Business")
    Category = apps.get_model("products", "Category")

    for business in Business.objects.all():
        for group, names in CATEGORIES.items():
            for name in names:
                Category.objects.get_or_create(
                    business=business,
                    name=name,
                    defaults={"group": group},
                )


def remove_categories(apps, schema_editor):
    Category = apps.get_model("products", "Category")

    names = [
        name
        for categories in CATEGORIES.values()
        for name in categories
    ]

    Category.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_category_options_category_group_product_brand"),
        ("businesses", "0002_alter_business_options"),
    ]

    operations = [
        migrations.RunPython(
            seed_categories,
            remove_categories,
        ),
    ]
