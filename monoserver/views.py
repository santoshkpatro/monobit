import time, json
from django.views import View
from django.http import StreamingHttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from monoserver.redis import client
from monoserver.models import Channel


class SSERelayView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        return JsonResponse(
            {"error": "Authentication required"},
            status=401,
        )

    def get(self, request, **kwargs):
        subscriptions = [
            f"monobit:channel:{channel_id}"
            for channel_id in Channel.objects.filter(
                memberships__user=request.user
            ).values_list("id", flat=True)
        ]

        # This is for user notifications
        subscriptions.append(request.user.notification_channel_key)

        def event_stream():
            subscriber = client.pubsub()

            try:
                subscriber.subscribe(*subscriptions)
                last_heartbeat = time.monotonic()

                while True:
                    message = subscriber.get_message(
                        ignore_subscribe_messages=True, timeout=1.0
                    )
                    if message:
                        payload = json.loads(message.get("data"))

                        yield f"event: {payload['type']}\n"
                        yield f"data: {json.dumps(payload['data'])}\n\n"

                    # SSE heartbeat
                    if time.monotonic() - last_heartbeat >= 15:
                        yield ": keep-alive\n\n"
                        last_heartbeat = time.monotonic()

            finally:
                subscriber.unsubscribe(*subscriptions)
                subscriber.close()

        response = StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream",
        )

        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"

        return response
