from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from monobit.models.config import Config
from monobit.config_loader import _get_config_value


@receiver(post_save, sender=Config)
@receiver(post_delete, sender=Config)
def clear_config_cache(sender, **kwargs):
    _get_config_value.cache_clear()
