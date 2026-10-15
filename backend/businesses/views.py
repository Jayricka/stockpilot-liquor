from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from businesses.models import (
    Business,
    BusinessInvitation,
    BusinessMembership,
)
from businesses.invitation_serializers import (
    BusinessInvitationAcceptSerializer,
    BusinessInvitationCreateSerializer,
    BusinessInvitationSerializer,
)
from businesses.serializers import (
    BusinessMemberCreateSerializer,
    BusinessMemberRoleSerializer,
    BusinessMemberSerializer,
    BusinessSerializer,
)
from businesses.services import (
    BusinessInvitationService,
    BusinessMembershipService,
    BusinessService,
)


class BusinessListCreateView(generics.ListCreateAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Business.objects.filter(
                memberships__user=self.request.user,
                memberships__is_active=True,
            ).distinct()
        )

    def perform_create(self, serializer):
        BusinessService.create_business(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )


class BusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "business_id"

    def get_queryset(self):
        return (
            Business.objects.filter(
                memberships__user=self.request.user,
                memberships__is_active=True,
            ).distinct()
        )


class BusinessMemberListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessMemberSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BusinessMemberCreateSerializer
        return BusinessMemberSerializer

    def get_queryset(self):
        return (
            BusinessMembership.objects.filter(
                business_id=self.kwargs["business_id"],
                business__is_active=True,
                business__memberships__user=self.request.user,
                business__memberships__is_active=True,
                is_active=True,
            )
            .select_related("user", "business")
            .order_by("created_at")
            .distinct()
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        membership = BusinessMembershipService.add_member(
            business_id=self.kwargs["business_id"],
            actor=request.user,
            email=serializer.validated_data["email"],
            role=serializer.validated_data["role"],
        )

        return Response(
            BusinessMemberSerializer(membership).data,
            status=status.HTTP_201_CREATED,
        )


class BusinessMemberDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessMemberRoleSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        membership = BusinessMembershipService.update_member_role(
            business_id=self.kwargs["business_id"],
            actor=request.user,
            user_id=self.kwargs["user_id"],
            role=serializer.validated_data["role"],
        )

        return Response(BusinessMemberSerializer(membership).data)

    def delete(self, request, *args, **kwargs):
        BusinessMembershipService.deactivate_member(
            business_id=self.kwargs["business_id"],
            actor=request.user,
            user_id=self.kwargs["user_id"],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class BusinessInvitationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        membership = BusinessMembership.objects.filter(
            business_id=self.kwargs["business_id"],
            business__is_active=True,
            user=self.request.user,
            is_active=True,
        ).first()

        if membership is None or membership.role not in (
            BusinessMembership.Role.OWNER,
            BusinessMembership.Role.MANAGER,
        ):
            raise ValidationError(
                "You do not have permission to view invitations."
            )

        now = timezone.now()
        BusinessInvitation.objects.filter(
            business_id=self.kwargs["business_id"],
            status=BusinessInvitation.Status.PENDING,
            expires_at__lte=now,
        ).update(
            status=BusinessInvitation.Status.EXPIRED,
            updated_at=now,
        )

        return BusinessInvitation.objects.filter(
            business_id=self.kwargs["business_id"],
            business__is_active=True,
        ).select_related("invited_by")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BusinessInvitationCreateSerializer
        return BusinessInvitationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invitation, raw_token = (
            BusinessInvitationService.create_invitation(
                business_id=self.kwargs["business_id"],
                actor=request.user,
                email=serializer.validated_data["email"],
                role=serializer.validated_data["role"],
            )
        )

        response_data = BusinessInvitationSerializer(
            invitation,
            context=self.get_serializer_context(),
        ).data
        return Response(
            {
                "invitation": response_data,
                "token": raw_token,
            },
            status=status.HTTP_201_CREATED,
        )


class BusinessInvitationDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        BusinessInvitationService.revoke_invitation(
            business_id=self.kwargs["business_id"],
            actor=request.user,
            invitation_id=self.kwargs["invitation_id"],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)



class BusinessInvitationAcceptView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessInvitationAcceptSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        BusinessInvitationService.accept_invitation(
            token=serializer.validated_data["token"],
            actor=request.user,
        )

        return Response(
            {"detail": "Invitation accepted."},
            status=status.HTTP_200_OK,
        )
