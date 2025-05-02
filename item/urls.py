from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('',views.browse, name='browse'),  # URL for the item browse view
    path('<int:pk>/', views.detail, name='detail'),  # URL for the item detail view
    path('new/', views.new, name='new'),  # URL for creating a new item
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),


]