from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item, Category
from django.contrib.auth.decorators import login_required
from .models import MyGame

@login_required
def my_games(request):
    owned_games = MyGame.objects.filter(user=request.user).select_related('product')
    # Récupérer toutes les catégories pour la section "Explore by category"
    categories = Category.objects.all()
    return render(request, 'my_games.html', {
        'games': owned_games,
        'categories': categories
    })