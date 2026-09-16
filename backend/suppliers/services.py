from django.db import transaction

from .models import Supplier


class SupplierService:

    @staticmethod
    @transaction.atomic
    def create_supplier(business, validated_data):
        name = validated_data["name"].strip()

        existing_supplier = Supplier.objects.filter(
            business=business,
            name__iexact=name,
        ).first()

        if existing_supplier:
            raise ValueError(
                "A supplier with this name already exists in this business."
            )

        validated_data["name"] = name

        return Supplier.objects.create(
            business=business,
            **validated_data,
        )

    @staticmethod
    @transaction.atomic
    def update_supplier(supplier, validated_data):
        name = validated_data.get(
            "name",
            supplier.name,
        ).strip()

        duplicate_supplier = Supplier.objects.filter(
            business=supplier.business,
            name__iexact=name,
        ).exclude(
            id=supplier.id,
        ).first()

        if duplicate_supplier:
            raise ValueError(
                "A supplier with this name already exists in this business."
            )

        validated_data["name"] = name

        for field, value in validated_data.items():
            setattr(supplier, field, value)

        supplier.save()

        return supplier
