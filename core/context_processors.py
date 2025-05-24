from .models import Category
from django.conf import settings

def media_url(request):
    return {
        'MEDIA_URL': settings.MEDIA_URL,
    }


def categories_processor(request):
    return {'categories': Category.objects.all()}