import redis

from django.conf import settings
from django.utils.functional import LazyObject


class RedisClient(LazyObject):
    def _setup(self):
        self._wrapped = redis.Redis.from_url(settings.REDIS_URL + "1")


client = RedisClient()