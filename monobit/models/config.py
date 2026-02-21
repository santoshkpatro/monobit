from django.db import models


class Config(models.Model):
    key = models.CharField(max_length=128, primary_key=True)
    value = models.JSONField()

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "config"

    def __str__(self):
        return self.key
