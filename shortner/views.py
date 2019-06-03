from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import DetailView

from .models import UrlShortener
from api.models import Document


class UrlRedirectView(View):
    '''View for retriving the actual  url'''

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(
            UrlShortener, shortcode=kwargs.get('shortcode'))
        document_url = document.url
        return HttpResponseRedirect(document_url)


class DocumentView(DetailView):
    context_object_name = 'document'
    model = Document
    template_name = "documents/document_details.html"
