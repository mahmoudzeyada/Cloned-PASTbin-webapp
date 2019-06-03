from django.core.management.base import BaseCommand, CommandError

from shortner.models import UrlShortener


class Command(BaseCommand):
    help = "refreshes all shorturl "

    def add_arguments(self, parser):
        parser.add_argument("--items", type=int)

    def handle(self, *args, **options):
        return UrlShortener.objects.refresh_all_shortcode(
            items=options['items'])
