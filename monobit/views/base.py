import json
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from monobit.models.config import Config


def index(request):
    context = {"debug": settings.DEBUG}
    if not settings.DEBUG:
        # if not settings.DEBUG:
        manifest_path = (
            Path(settings.BASE_DIR)
            / "monobit"
            / "static"
            / "monobit"
            / ".vite"
            / "manifest.json"
        )

        with open(manifest_path) as f:
            manifest = json.load(f)

        entry = manifest["index.html"]

        context["vite_js"] = settings.STATIC_URL + "monobit/" + entry["file"]

        context["vite_css"] = [
            settings.STATIC_URL + "monobit/" + css for css in entry.get("css", [])
        ]

    return render(request, "index.html", context)


class ConfigAPIView(APIView):
    def get(self, request, *args, **kwargs):
        configs = Config.objects.filter(
            key__in=["organization_name", "organization_email", "contact_email"]
        )
        data = {}
        for config in configs:
            data[config.key] = config.value
        return Response(data=data, status=status.HTTP_200_OK)
