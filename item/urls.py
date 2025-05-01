from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),  # URL for the item detail view
    path('new/', views.new, name='new'),  # URL for creating a new item


]