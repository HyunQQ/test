from django.db import models


class InqMessage(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    message = models.TextField()
    channel_id = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
    created_at = models.CharField(max_length=64)


class InqChannels(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)


class InqChannelToUsers(models.Model):
    channel_id = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
