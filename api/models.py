from django.db import models
from django.conf import settings


class Document (models.Model):
    past = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name="owner_pasts",
                              blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SharedDocuments(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
