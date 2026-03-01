import socket
import signal
import time
from django.db import transaction
from django.utils import timezone

from monobit.models.job import Job
from monobit.models.choices import JobStatus
from monobit.worker.processing import process_payload


class Worker:
    def __init__(
        self,
        worker_id=None,
        batch_size=50,
        poll_interval=1,
        max_retries=5,
        lock_timeout_seconds=5,
    ):
        self.worker_id = worker_id or socket.gethostname()
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        self.max_retries = max_retries
        self.lock_timeout_seconds = lock_timeout_seconds

        self._running = True

        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)

    def _shutdown(self, *args):
        print("Gracefully shutting down worker...")
        self._running = False

    def run(self):
        print(f"Worker started: {self.worker_id}")

        while self._running:
            self._requeue_stale_jobs()

            jobs = Job.fetch_jobs(
                batch_size=self.batch_size,
                worker_id=self.worker_id,
            )

            if not jobs:
                time.sleep(self.poll_interval)
                continue

            for job in jobs:
                self._process(job)

        print("Worker stopped.")

    def _process(self, job):
        try:
            with transaction.atomic():
                process_payload(job.payload)

                job.status = JobStatus.COMPLETED
                job.locked_at = None
                job.locked_by = None
                job.error = None

                job.save(update_fields=["status", "locked_at", "locked_by", "error"])

        except Exception as exc:
            self._handle_failure(job, exc)

    def _handle_failure(self, job, exc):
        job.retry_count += 1
        job.error = str(exc)

        if job.retry_count >= self.max_retries:
            job.status = JobStatus.FAILED
        else:
            delay = min(60, 2**job.retry_count)
            job.status = JobStatus.PENDING
            job.available_at = timezone.now() + timezone.timedelta(seconds=delay)

        job.locked_at = None
        job.locked_by = None

        job.save(
            update_fields=[
                "status",
                "retry_count",
                "available_at",
                "error",
                "locked_at",
                "locked_by",
            ]
        )
