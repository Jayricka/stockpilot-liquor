from rest_framework import serializers

from .models import Business, BusinessMembership


class BusinessSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = [
            "id",
            "name",
            "business_type",
            "phone",
            "email",
            "address",
            "license_number",
            "is_active",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "role",
            "created_at",
            "updated_at",
        ]

    def get_role(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return None

        membership = (
            BusinessMembership.objects
            .filter(
                business=obj,
                user=request.user,
                is_active=True,
            )
            .first()
        )

        return membership.role if membership else None
