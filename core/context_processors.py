from .models import Category
from django.conf import settings

def media_url(request):
    return {
        'MEDIA_URL': settings.MEDIA_URL,
    }


def categories(request):
    return {'categories': Category.objects.all()}