# views.py
import json
from pathlib import Path
from django.conf import settings
from django.shortcuts import render


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
