from django.db import models
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.conf import settings

from monoserver.models.base import BaseTimestampModel
from monoserver.models.fields import PrefixedPrimaryKeyField
from monoserver.models.choices import ChannelVisibility, ChannelMembershipRole


class Channel(BaseTimestampModel):
    id = PrefixedPrimaryKeyField(prefix="chn")
    name = models.CharField(max_length=182, blank=True, null=True)
    visibility = models.CharField(
        max_length=16,
        choices=ChannelVisibility.choices,
        default=ChannelVisibility.PRIVATE,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_channels",
        blank=True,
        null=True,
    )
    direct_key = models.CharField(max_length=128, blank=True, null=True)

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ChannelMembership",
        related_name="channels",
    )

    class Meta:
        db_table = "channels"
        indexes = [models.Index(fields=["visibility"], name="idx_channel_visibility")]
        constraints = [
            models.UniqueConstraint(
                fields=["direct_key"],
                condition=models.Q(visibility=ChannelVisibility.DIRECT),
                name="uq_channel_direct_key",
            ),
        ]

    @classmethod
    def generate_direct_key(cls, user_a, user_b):
        return ":".join(sorted([str(user_a.pk), str(user_b.pk)]))


class ChannelMembership(BaseTimestampModel):
    id = PrefixedPrimaryKeyField(prefix="chmb")
    channel = models.ForeignKey(
        "Channel", on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=16,
        choices=ChannelMembershipRole.choices,
        default=ChannelMembershipRole.COLLABORATOR,
    )

    class Meta:
        db_table = "channel_memberships"
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "user"],
                name="uq_channel_membership",
            ),
        ]
