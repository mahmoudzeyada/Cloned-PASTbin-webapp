import string
import random

from django.conf import settings

SHORT_URL_MIN = getattr("settings", "SHORT_URL_MIN", 6)


def create_shortcode(instance,
                     chars=string.ascii_lowercase+string.digits,
                     size=SHORT_URL_MIN):

    new_code = "".join(random.choice(chars) for _ in range(size))
    klass = instance.__class__
    qs_exists = klass.objects.filter(shortcode=new_code).exists()
    if qs_exists:
        return create_shortcode()
    return new_code
