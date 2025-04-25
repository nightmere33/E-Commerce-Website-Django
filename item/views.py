from django.shortcuts import render , get_object_or_404
from .models import Item
# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk )
    related_items = Item.objects.filter(Category=item.Category,is_sold=False).exclude(pk=pk)[0:3]
    return render(request ,'item/detail.html', {
        'item':item,
        'related_items':related_items,
    })