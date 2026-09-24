import uuid

from django.conf import settings
from django.db import models

from businesses.models import Business


class DemoSession(models.Model):
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="demo_session",
    )

    business = models.OneToOneField(
        Business,
        on_delete=models.CASCADE,
        related_name="demo_session",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    last_used_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Demo session {self.token}"
