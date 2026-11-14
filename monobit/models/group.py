from django.db import models
from django.conf import settings

from monobit.models.base import BaseTimestampModel
from monobit.models.fields import PrefixedPrimaryKeyField


class Group(BaseTimestampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="group",
    )
    description = models.TextField(blank=True, default="")
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="GroupMembership",
        related_name="groups",
    )

    class Meta:
        db_table = "groups"


class GroupMembership(BaseTimestampModel):
    id = PrefixedPrimaryKeyField(prefix="grpm")

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_memberships",
    )

    class Meta:
        db_table = "group_memberships"

        constraints = [
            models.UniqueConstraint(
                fields=["group", "user"],
                name="uq_group_membership",
            ),
        ]
