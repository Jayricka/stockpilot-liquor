from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Business,
    BusinessMembership,
)
from .permissions import (
    CanManageBusiness,
    CanManageMembers,
)
from .serializers import (
    AddBusinessMemberSerializer,
    BusinessMemberSerializer,
    BusinessSerializer,
    ChangeBusinessMemberRoleSerializer,
)
from .services.businesses import BusinessService
from .services.memberships import (
    BusinessMembershipService,
)


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
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        try:
            self.perform_create(serializer)
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = self.get_serializer(
            self.created_business,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class BusinessDetailView(
    generics.RetrieveUpdateAPIView,
):
    serializer_class = BusinessSerializer
    permission_classes = [
        IsAuthenticated,
        CanManageBusiness,
    ]
    lookup_url_kwarg = "business_id"

    def get_queryset(self):
        return Business.objects.filter(
            memberships__user=self.request.user,
            memberships__is_active=True,
        ).distinct()


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


class BusinessMemberCreateView(
    generics.CreateAPIView,
):
    serializer_class = AddBusinessMemberSerializer
    permission_classes = [
        IsAuthenticated,
        CanManageMembers,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        try:
            business = Business.objects.get(
                id=kwargs["business_id"],
            )

            membership = (
                BusinessMembershipService.add_member(
                    business=business,
                    email=serializer.validated_data["email"],
                    role=serializer.validated_data["role"],
                )
            )
        except Business.DoesNotExist:
            return Response(
                {"detail": "Business not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = (
            BusinessMemberSerializer(
                membership,
            )
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class BusinessMemberRoleUpdateView(
    generics.UpdateAPIView,
):
    serializer_class = ChangeBusinessMemberRoleSerializer
    permission_classes = [
        IsAuthenticated,
        CanManageMembers,
    ]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        try:
            business = Business.objects.get(
                id=kwargs["business_id"],
            )

            membership = (
                BusinessMembershipService.change_role(
                    business=business,
                    user_id=kwargs["user_id"],
                    role=serializer.validated_data["role"],
                )
            )
        except Business.DoesNotExist:
            return Response(
                {"detail": "Business not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            BusinessMemberSerializer(
                membership,
            ).data,
        )


class BusinessMemberDeactivateView(
    generics.DestroyAPIView,
):
    permission_classes = [
        IsAuthenticated,
        CanManageMembers,
    ]

    def destroy(self, request, *args, **kwargs):
        try:
            business = Business.objects.get(
                id=kwargs["business_id"],
            )

            BusinessMembershipService.deactivate_member(
                business=business,
                user_id=kwargs["user_id"],
            )
        except Business.DoesNotExist:
            return Response(
                {"detail": "Business not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
