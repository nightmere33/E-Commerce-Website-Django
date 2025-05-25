
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from django.contrib.auth.decorators import login_required
from .models import MyGame
# Create your views here.

@login_required
def my_games(request):
    owned_games = MyGame.objects.filter(user=request.user)
    return render(request, 'my_games.html', {'games': owned_games})
