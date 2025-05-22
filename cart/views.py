from django.shortcuts import render,get_object_or_404,redirect
from.cart import Cart

from item.models import Item
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.

def cart_summary(request):
    #get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    total = 0
    for product in cart_products:
        product.line_total = float(product.price) * product.quantity
        total += product.line_total

    platform_cut = round(total * 0.05, 2)
    grand_total = round(total + platform_cut, 2)

    return render(request, 'cart_summary.html', {
        "cart_products": cart_products,
        "total": total,
        "platform_cut": platform_cut,
        "grand_total": grand_total
    })
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



@require_POST
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
		# Get stuff
        product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response

def cart_update(request):
    pass