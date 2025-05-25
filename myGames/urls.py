from django.urls import path
from . import views  # ou from myGames import views selon ta structure

urlpatterns = [
    path('', views.my_games, name='my_games'),
]
