import os
import socket
from typing import List
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from monobit.models.worker import WorkerInstance, WorkerNode
from monobit.models.choices import WorkerInstanceStatus


class Command(BaseCommand):
    help = "Worker node reconciliation agent"

    HEARTBEAT_TIMEOUT = 30

    def handle(self, *args, **options):
        hostname = socket.gethostname()
        node: WorkerNode = self._register_node(hostname)

        if not node.is_enabled:
            return

        self._reconsile(node)

    def _register_node(self, hostname) -> WorkerNode:
        node, _ = WorkerNode.objects.get_or_create(
            hostname=hostname,
            defaults={"cpu_cores": os.cpu_count(), "is_enabled": False},
        )

        return node

    @transaction.atomic
    def _reconsile(self, node: WorkerNode):
        node = WorkerNode.objects.select_for_update().get(id=node.id)
        instances: List[WorkerInstance] = (
            WorkerInstance.objects.select_for_update().filter(worker_node=node)
        )
        pass
