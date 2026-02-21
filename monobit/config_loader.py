import os
import json
from functools import lru_cache
from django.apps import apps
from django.conf import settings


# Path to config.json in project root
CONFIG_PATH = os.path.join(settings.BASE_DIR, "config.json")


@lru_cache(maxsize=1)
def load_defaults():
    if not os.path.exists(CONFIG_PATH):
        return {}

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


@lru_cache(maxsize=256)
def _get_config_value(key):
    # Lazy model loading (prevents AppRegistryNotReady)
    Config = apps.get_model("monobit", "Config")

    # 1️⃣ Database override
    try:
        return Config.objects.get(key=key).value
    except Config.DoesNotExist:
        pass

    # 2️⃣ config.json fallback
    defaults = load_defaults()
    if key in defaults:
        return defaults[key]

    raise AttributeError(f"Config key '{key}' not found")


class ConfigProxy:
    def __getattr__(self, key):
        return _get_config_value(key)
