from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from businesses.models import Business
from .models import DeliveryOrder
from .serializers import DeliveryOrderSerializer
from .services import DeliveryService


class BusinessAccessMixin:

    def get_business(self):
        return get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )


class DeliveryListCreateView(
    BusinessAccessMixin,
    generics.ListCreateAPIView,
):
    serializer_class = DeliveryOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business = self.get_business()

        queryset = (
            DeliveryOrder.objects
            .filter(business=business)
            .select_related(
                "sale",
                "assigned_to",
            )
        )

        delivery_status = self.request.query_params.get(
            "status"
        )

        if delivery_status:
            queryset = queryset.filter(
                status=delivery_status
            )

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["business"] = self.get_business()
        return context

    def create(self, request, *args, **kwargs):
        business = self.get_business()

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            delivery = DeliveryService.create_delivery(
                business=business,
                user=request.user,
                validated_data=serializer.validated_data,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = self.get_serializer(
            delivery
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class DeliveryDetailView(
    BusinessAccessMixin,
    generics.RetrieveAPIView,
):
    serializer_class = DeliveryOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business = self.get_business()

        return (
            DeliveryOrder.objects
            .filter(business=business)
            .select_related(
                "sale",
                "assigned_to",
            )
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["business"] = self.get_business()
        return context


class AssignDeliveryView(
    BusinessAccessMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]

    def post(self, request, business_id, pk):
        business = self.get_business()

        delivery = get_object_or_404(
            DeliveryOrder,
            id=pk,
            business=business,
        )

        user_id = request.data.get("assigned_to")

        if not user_id:
            return Response(
                {
                    "detail": (
                        "assigned_to is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        from accounts.models import User

        user = get_object_or_404(
            User,
            id=user_id,
        )

        try:
            delivery = DeliveryService.assign_delivery(
                delivery_id=delivery.id,
                user=user,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DeliveryOrderSerializer(
            delivery,
            context={
                "request": request,
                "business": business,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class StartDeliveryView(
    BusinessAccessMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]

    def post(self, request, business_id, pk):
        business = self.get_business()

        delivery = get_object_or_404(
            DeliveryOrder,
            id=pk,
            business=business,
        )

        try:
            delivery = DeliveryService.start_delivery(
                delivery_id=delivery.id,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DeliveryOrderSerializer(
            delivery,
            context={
                "request": request,
                "business": business,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CompleteDeliveryView(
    BusinessAccessMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]

    def post(self, request, business_id, pk):
        business = self.get_business()

        delivery = get_object_or_404(
            DeliveryOrder,
            id=pk,
            business=business,
        )

        try:
            delivery = DeliveryService.complete_delivery(
                delivery_id=delivery.id,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DeliveryOrderSerializer(
            delivery,
            context={
                "request": request,
                "business": business,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CancelDeliveryView(
    BusinessAccessMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]

    def post(self, request, business_id, pk):
        business = self.get_business()

        delivery = get_object_or_404(
            DeliveryOrder,
            id=pk,
            business=business,
        )

        try:
            delivery = DeliveryService.cancel_delivery(
                delivery_id=delivery.id,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DeliveryOrderSerializer(
            delivery,
            context={
                "request": request,
                "business": business,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
