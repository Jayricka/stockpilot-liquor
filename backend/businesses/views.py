from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Business,
    BusinessMembership,
)
from .serializers import (
    BusinessMemberSerializer,
    BusinessSerializer,
)
from .services import BusinessService


class BusinessListCreateView(
    generics.ListCreateAPIView,
):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.filter(
            memberships__user=self.request.user,
            memberships__is_active=True,
        ).distinct()

    def perform_create(self, serializer):
        self.created_business = (
            BusinessService.create_business(
                user=self.request.user,
                validated_data=serializer.validated_data,
            )
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        try:
            self.perform_create(serializer)
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = self.get_serializer(
            self.created_business
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class BusinessMemberListView(
    generics.ListAPIView,
):
    serializer_class = BusinessMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            BusinessMembership.objects
            .filter(
                business_id=self.kwargs["business_id"],
                business__memberships__user=self.request.user,
                business__memberships__is_active=True,
                is_active=True,
            )
            .select_related("user")
            .order_by(
                "user__first_name",
                "user__last_name",
            )
        )
