from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from .models import DemoSession
from .serializers import (
    DemoActionSerializer,
    DemoProductSerializer,
)
from .services import DemoService


class DemoStartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session = DemoService.create_session()

        return Response(
            {
                "token": str(session.token),
                "business": {
                    "id": session.business.id,
                    "name": session.business.name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class DemoStateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            session = DemoService.get_session(token)
        except (
            DemoSession.DoesNotExist,
            ValueError,
        ) as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_404_NOT_FOUND,
            )

        session.last_used_at = timezone.now()
        session.save(
            update_fields=["last_used_at"]
        )

        products = Product.objects.filter(
            business=session.business,
            is_active=True,
        )

        return Response(
            {
                "business": {
                    "id": session.business.id,
                    "name": session.business.name,
                },
                "products": DemoProductSerializer(
                    products,
                    many=True,
                ).data,
            }
        )


class DemoPurchaseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            session = DemoService.get_session(token)
        except (
            DemoSession.DoesNotExist,
            ValueError,
        ) as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DemoActionSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        try:
            purchase = DemoService.receive_stock(
                session=session,
                **serializer.validated_data,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = purchase.items.first().product

        return Response(
            {
                "message": "Stock received successfully.",
                "product": DemoProductSerializer(
                    product
                ).data,
            }
        )


class DemoSaleView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            session = DemoService.get_session(token)
        except (
            DemoSession.DoesNotExist,
            ValueError,
        ) as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DemoActionSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        try:
            sale = DemoService.make_sale(
                session=session,
                **serializer.validated_data,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = sale.items.first().product

        return Response(
            {
                "message": "Sale completed successfully.",
                "sale": {
                    "invoice_number":
                        sale.invoice_number,
                    "total_amount":
                        sale.total_amount,
                    "gross_profit":
                        sale.gross_profit,
                },
                "product": DemoProductSerializer(
                    product
                ).data,
            }
        )
