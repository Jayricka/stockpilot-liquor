from django.urls import reverse
from rest_framework.test import APITestCase

from demo.services import DemoService


class DemoAPITestBase(APITestCase):
    def setUp(self):
        self.session = DemoService.create_session()

        self.product = (
            self.session.business.products
            .order_by("id")
            .first()
        )

        self.start_url = reverse(
            "demo-start"
        )

        self.state_url = reverse(
            "demo-state",
            kwargs={
                "token": self.session.token,
            },
        )

        self.purchase_url = reverse(
            "demo-purchase",
            kwargs={
                "token": self.session.token,
            },
        )

        self.sale_url = reverse(
            "demo-sale",
            kwargs={
                "token": self.session.token,
            },
        )
