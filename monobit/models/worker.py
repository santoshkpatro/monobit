from django.db import models
from django.utils import timezone

from monobit.models.base import BaseUUIDTimestampModel
from monobit.models.choices import WorkerInstanceStatus


class WorkerNode(BaseUUIDTimestampModel):
    hostname = models.CharField(max_length=225, unique=True)
    is_enabled = models.BooleanField(default=False)
    desired_workers = models.IntegerField(default=1)
    cpu_cores = models.PositiveIntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "worker_nodes"

    def __str__(self):
        return f"{self.hostname} (enabled={self.is_enabled}, desired={self.desired_workers})"


class WorkerInstance(BaseUUIDTimestampModel):
    worker_node = models.ForeignKey(
        "WorkerNode", on_delete=models.CASCADE, related_name="instances"
    )
    worker_index = models.PositiveIntegerField()
    worker_id = models.CharField(max_length=150, unique=True)
    pid = models.IntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=WorkerInstanceStatus.choices,
        default=WorkerInstanceStatus.STARTING,
    )
    started_at = models.DateTimeField(null=True, blank=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    restart_count = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=False)

    class Meta:
        db_table = "worker_instances"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["last_heartbeat"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["worker_node", "worker_index"],
                name="unique_worker_index_per_node",
            )
        ]
