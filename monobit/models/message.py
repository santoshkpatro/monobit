from django.db import models
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.conf import settings

from monobit.models.base import BaseTimestampModel
from monobit.models.fields import PrefixedPrimaryKeyField


class Message(BaseTimestampModel):
    id = PrefixedPrimaryKeyField(prefix="msg")
    channel = models.ForeignKey(
        "Channel", on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sent_messages"
    )
    content = models.TextField(blank=True, default="")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "messages"
        indexes = [
            models.Index(
                fields=["channel", "-created_at"],
                name="idx_message_channel_created",
            ),
        ]
