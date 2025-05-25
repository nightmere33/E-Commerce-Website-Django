from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    items = Item.objects.filter(created_by = request.user)

    return render(request, 'dashboard/index.html', {
        'items': items,
    })

<<<<<<< HEAD
=======

>>>>>>> 73ca047f2a58b743c6006f48a332eb4dc71b8aa2

