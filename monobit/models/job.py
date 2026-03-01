from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from monobit.models.base import BaseUUIDTimestampModel
from monobit.models.choices import JobStatus


class Job(BaseUUIDTimestampModel):
    payload = models.JSONField(default=dict)
    status = models.CharField(
        max_length=16, choices=JobStatus.choices, default=JobStatus.PENDING
    )
    retry_count = models.IntegerField(default=0)
    available_at = models.DateTimeField(auto_now_add=True)
    locked_at = models.DateTimeField(blank=True, null=True)
    locked_by = models.CharField(max_length=64, blank=True, null=True)
    error = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "jobs"
        indexes = [
            models.Index(
                fields=["available_at"],
                name="jobs_pending_available_idx",
                condition=Q(status=JobStatus.PENDING),
            )
        ]

    @classmethod
    def fetch_jobs(cls, batch_size=10, worker_id=None):
        with transaction.atomic():
            jobs = (
                cls.objects.select_for_update(skip_locked=True)
                .filter(status=JobStatus.PENDING, available_at__lte=timezone.now())
                .order_by("available_at")[:batch_size]
            )
            jobs = list(jobs)
            for job in jobs:
                job.status = JobStatus.PROCESSING
                job.locked_at = timezone.now()
                job.locked_by = worker_id

            cls.objects.bulk_update(jobs, ["status", "locked_at", "locked_by"])

        return jobs
