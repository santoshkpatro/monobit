import uuid
from functools import partial

from django.db import models


class PrefixedPrimaryKeyField(models.CharField):
    MAX_LENGTH = 48
    UUID_LENGTH = 32
    MAX_PREFIX_LENGTH = MAX_LENGTH - UUID_LENGTH - 1

    def __init__(self, prefix, *args, **kwargs):
        prefix = prefix.lower()

        if not prefix or len(prefix) > self.MAX_PREFIX_LENGTH:
            raise ValueError(
                f"Prefix must contain 1-{self.MAX_PREFIX_LENGTH} characters."
            )

        self.prefix = prefix

        kwargs.setdefault("max_length", self.MAX_LENGTH)
        kwargs.setdefault("primary_key", True)
        kwargs.setdefault("editable", False)
        kwargs.setdefault("default", partial(self.generate, prefix))

        super().__init__(*args, **kwargs)

    @staticmethod
    def generate(prefix):
        return f"{prefix}_{uuid.uuid7().hex}"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        kwargs["prefix"] = self.prefix
        kwargs.pop("default", None)

        return name, path, args, kwargs
