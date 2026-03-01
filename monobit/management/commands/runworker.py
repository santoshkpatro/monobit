# monobit/management/commands/runworker.py

from django.core.management.base import BaseCommand
from monobit.worker import Worker


class Command(BaseCommand):
    help = "Run Monobit worker"

    def add_arguments(self, parser):
        parser.add_argument(
            "--worker-id",
            type=str,
            help="Optional worker identifier",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=50,
            help="Number of jobs to fetch per batch",
        )
        parser.add_argument(
            "--poll-interval",
            type=int,
            default=1,
            help="Polling interval in seconds",
        )

    def handle(self, *args, **options):
        worker = Worker(
            worker_id=options.get("worker_id"),
            batch_size=options.get("batch_size"),
            poll_interval=options.get("poll_interval"),
        )
        worker.run()
