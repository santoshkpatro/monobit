from django.db import models

from monobit.models.base import BaseUUIDTimestampModel


class Event(BaseUUIDTimestampModel):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="events"
    )
    issue = models.ForeignKey("Issue", on_delete=models.SET_NULL, null=True)
    properties = models.JSONField(default=dict)
    hash = models.CharField(max_length=128)

    class Meta:
        db_table = "events"
