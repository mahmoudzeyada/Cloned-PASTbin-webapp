import csv

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView
from django.contrib.auth import get_user_model

from .models import UrlShortener
from api.models import Document


User = get_user_model()


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


class CsvView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="file.csv"'

        fieldnames = ["number_of_pasts", "number_of_users"]
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        number_of_pasts = Document.objects.all().count()
        number_of_users = User.objects.all().count()
        writer.writerow({"number_of_pasts": number_of_pasts,
                         "number_of_users": number_of_users})

        fieldnames = ["username", "number_of_pasts"]
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        qs = User.objects.all()
        for user in qs:
            username = user.username
            number_of_pasts = Document.objects.filter(owner=user).count()
            writer.writerow({"username": username,
                             "number_of_pasts": number_of_pasts})

        fieldnames = ['document_id', 'owner',
                      'past', 'number_of_sharing', 'number']
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        qs = Document.objects.all()
        for document in qs:
            number_of_sharing = document.shared_document.all().count()
            writer.writerow({'document_id': document.id,
                             'owner': document.owner,
                             'past': document.past,
                             "number_of_sharing": number_of_sharing})

        return response
