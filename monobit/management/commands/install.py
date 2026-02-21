import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from monobit.models.config import Config


CONFIG_PATH = os.path.join(settings.BASE_DIR, "config.json")


class Command(BaseCommand):
    help = "Initial installation: seed config.json into database"

    @transaction.atomic
    def handle(self, *args, **options):
        if not os.path.exists(CONFIG_PATH):
            self.stdout.write(
                self.style.ERROR("config.json not found in project root.")
            )
            return

        with open(CONFIG_PATH, "r") as f:
            defaults = json.load(f)

        created_count = 0

        for key, value in defaults.items():
            _, created = Config.objects.get_or_create(
                key=key,
                defaults={"value": value},
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Install complete. {created_count} new config keys added."
            )
        )
