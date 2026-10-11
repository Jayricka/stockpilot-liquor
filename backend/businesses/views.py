from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from businesses.models import Business, BusinessMembership
from businesses.serializers import (
    BusinessMemberCreateSerializer,
    BusinessMemberRoleSerializer,
    BusinessMemberSerializer,
    BusinessSerializer,
)
from businesses.services import (
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
