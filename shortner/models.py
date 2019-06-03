from django.db import models
from django.conf import settings
from .utils import create_shortcode
from api.models import Document


SHORT_URL_MAX = getattr(settings, "SHORT_URL_MAX ", 15)


class CustomManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super().all(*args, **kwargs)
        return qs.filter(active=True)

    def refresh_all_shortcode(self, items=None):
        qs = UrlShortener.objects.filter(id__gte=1)
        if items is not None or isinstance(items, int):
            qs = qs.order_by("-id")[:items]
        new_code = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            q.save()
            print(q)
            new_code += 1
        return f"New codes generated:{new_code}"


class UrlShortener(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    url = models.CharField(max_length=220, blank=True)
    shortcode = models.CharField(
        max_length=SHORT_URL_MAX, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = CustomManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
            self.url = "http://127.0.0.1:8000"+self.document.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.url} => {self.shortcode}"
