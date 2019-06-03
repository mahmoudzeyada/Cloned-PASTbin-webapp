from django.contrib import admin

from .models import Document, SharedDocuments

admin.site.register(Document)
admin.site.register(SharedDocuments)
