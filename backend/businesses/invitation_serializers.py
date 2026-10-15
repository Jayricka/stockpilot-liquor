from rest_framework import serializers

from .models import BusinessInvitation


class BusinessInvitationCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=[
            BusinessInvitation.Role.MANAGER,
            BusinessInvitation.Role.STAFF,
        ],
    )

    def validate_email(self, value):
        return value.strip().lower()


class BusinessInvitationSerializer(serializers.ModelSerializer):
    invited_by_email = serializers.EmailField(
        source="invited_by.email",
        read_only=True,
    )

    class Meta:
        model = BusinessInvitation
        fields = [
            "id",
            "email",
            "role",
            "status",
            "invited_by_email",
            "expires_at",
            "accepted_at",
            "created_at",
        ]
        read_only_fields = fields


class BusinessInvitationCreatedSerializer(
    BusinessInvitationSerializer,
):
    token = serializers.CharField(read_only=True)

    class Meta(BusinessInvitationSerializer.Meta):
        fields = [
            *BusinessInvitationSerializer.Meta.fields,
            "token",
        ]



class BusinessInvitationAcceptSerializer(serializers.Serializer):
    token = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )
