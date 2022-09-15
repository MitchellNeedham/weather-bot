import uuid
from datetime import datetime, timezone

from django.db import models
from django_db_cascade.deletions import DB_CASCADE
from django.contrib.postgres.fields import ArrayField


class Conversation(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
    start_time = models.DateTimeField()
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    location_name = models.CharField(max_length=128, blank=True, null=True)
    weather_response = models.JSONField(blank=True, null=True)
    weather_request_time = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.start_time:
            self.start_time = datetime.now().astimezone(tz=timezone.utc)
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)


class Message(models.Model):
    conversation = models.ForeignKey("Conversation", on_delete=DB_CASCADE)
    message = models.TextField()
    response = ArrayField(models.TextField(), default=list)
    time = models.DateTimeField(blank=True, null=True)
    action_requested = models.CharField(max_length=24, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.time:
            self.time = datetime.now().astimezone(tz=timezone.utc)
        super().save(*args, **kwargs)
