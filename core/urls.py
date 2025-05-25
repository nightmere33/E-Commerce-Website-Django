from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm  # Assurez-vous d'importer votre formulaire personnalisé
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.termsofuse, name='termsofuse'),  # Assurez-vous que ce nom est cohérent
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html', 
        authentication_form=LoginForm,  # Utilisez votre formulaire personnalisé
        next_page='core:index'
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path("chatbot/", views.chatbot, name="chatbot"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

