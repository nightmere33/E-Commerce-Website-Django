from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
app_name = 'core'

urlpatterns=[

    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:index'), name='logout'),
    path('privacy/', views.privacy, name='privacy'),
    path('termsofuse/', views.termsofuse, name='termsofuse'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]