from django.shortcuts import render,get_object_or_404
from.cart import Cart

from item.models import Item
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    return render(request, 'cart_summary.html',{})

def cart_add(request):
    #get the cart
    cart = Cart(request)
    # test for post
    if request.POST.get('action')== 'post':
        #get the items
        product_id = int(request.POST.get('product_id'))
        #lookup product in db
        product = get_object_or_404(Item, id=product_id)
        #save to a session
        cart.add(product=product)
        #get cart quantitiy
        cart_quantity = cart.__len__()
        #return a json response
        #response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty' :  cart_quantity})
        return response



def cart_delete(request):
    pass

def cart_update(request):
    pass