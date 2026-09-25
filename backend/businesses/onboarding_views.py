from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from billing.serializers import SubscriptionSerializer

from .onboarding_serializers import (
    BusinessOnboardingSerializer,
)


class BusinessOnboardingView(generics.CreateAPIView):
    serializer_class = BusinessOnboardingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        business = serializer.save()

        subscription = serializer.subscription

        return Response(
            {
                "business": {
                    "id": business.id,
                    "name": business.name,
                    "business_type": (
                        business.business_type
                    ),
                    "phone": business.phone,
                    "email": business.email,
                    "address": business.address,
                    "license_number": (
                        business.license_number
                    ),
                },
                "subscription": SubscriptionSerializer(
                    subscription
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )
