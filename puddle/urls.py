
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('core.urls')),  # URL for the index view
    path('item/', include('item.urls')),  # Include item app URLs
    path('dashboard/', include('dashboard.urls')),  # Include dashboard app URLs
    path('inbox/', include('conversation.urls')),  # Include conversation app URLs
    path('admin/', admin.site.urls),
   

] + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
