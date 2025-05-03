from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
     path('new/<int:item_pk>/', views.new_conversation, name='new'), # URL pattern for new conversation view
     
     path('',views.inbox, name='inbox'), # URL pattern for inbox view
     path('<int:pk>/',views.detail, name='detail'), # URL pattern for conversation detail view
]
