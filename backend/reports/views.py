from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from businesses.models import Business

from .serializers import DashboardSerializer
from .services import DashboardService


class DashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardSerializer

    def get_business(self):
        return get_object_or_404(
            Business,
            id=self.kwargs["business_id"],
            memberships__user=self.request.user,
            memberships__is_active=True,
        )

    def get(self, request, business_id):
        business = self.get_business()

        dashboard = DashboardService.get_dashboard(
            business=business,
        )

        serializer = self.get_serializer(
            dashboard,
        )

        return Response(serializer.data)
