import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

import tornado.web
import tornado.ioloop

from django.core.management.base import BaseCommand
from monobit.relay.handlers import RelayHandler


class Command(BaseCommand):

    help = "Starts the Relay WebSocket server."

    def handle(self, *args, **options):

        app = tornado.web.Application([
            (r"/ws/", RelayHandler),
        ])

        server = app.listen(8001, address="0.0.0.0")
        io_loop = tornado.ioloop.IOLoop.current()

        self.stdout.write(
            self.style.SUCCESS("Relay server running on port 8001")
        )

        try:
            io_loop.start()

        except KeyboardInterrupt:
            self.stdout.write("\nStopping Relay server...")

        finally:
            server.stop()
            io_loop.stop()

            self.stdout.write(
                self.style.SUCCESS("Relay server stopped.")
            )