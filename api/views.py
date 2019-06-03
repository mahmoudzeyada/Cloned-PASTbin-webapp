from django.shortcuts import render

from rest_framework import permissions, viewsets
from rest_framework import mixins
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import DocumentSerializer, SharedDocumentsSerializer
from .models import Document, SharedDocuments
from .permissions import IsOwner
from .filters import DateFilter


class DocumentViewSet(viewsets.ModelViewSet):

    ''' model view for Document '''
    serializer_class = DocumentSerializer
    permission_classes = (IsOwner,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = DateFilter
    ordering_fields = ('created_at', 'updated_at')
    ordering = ('updated_at')

    def get_queryset(self):
        shared_document = SharedDocuments.objects\
            .filter(users=self.request.user)\
            .values_list("document", flat=True)
        return Document.objects.filter(id__in=shared_document)
