from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from businesses.models import Business, BusinessMembership
from businesses.serializers import (
    BusinessMemberSerializer,
    BusinessSerializer,
)
from businesses.services import BusinessService


class BusinessListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Business.objects
            .filter(
                memberships__user=self.request.user,
                memberships__is_active=True,
            )
            .distinct()
        )

    def perform_create(self, serializer):
        BusinessService.create_business(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )


class BusinessDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Business.objects
            .filter(
                memberships__user=self.request.user,
                memberships__is_active=True,
            )
            .distinct()
        )


class BusinessMemberListView(
    generics.ListAPIView
):
    serializer_class = BusinessMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business_id = self.kwargs["business_id"]

        return (
            BusinessMembership.objects
            .filter(
                business_id=business_id,
                business__memberships__user=self.request.user,
                business__memberships__is_active=True,
            )
            .select_related("user", "business")
            .order_by("created_at")
        )


class BusinessOnboardingView(
    generics.CreateAPIView
):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        business = BusinessService.create_business(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        output_serializer = self.get_serializer(
            business
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )
