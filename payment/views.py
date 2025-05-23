from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from decimal import Decimal

@login_required
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    
    # Calculate totals
    total = 0
    for product in cart_products:
        product.line_total = float(product.price) * product.quantity
        total += product.line_total

    platform_cut = round(total * 0.05, 2)
    grand_total = round(total + platform_cut, 2)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_paid = Decimal(grand_total)
            order.save()
            
            # Create order items
            for product in cart_products:
                OrderItem.objects.create(
                    order=order,
                    product_id=product.id,
                    price=product.price,
                    quantity=product.quantity
                )
            
            # Clear the cart
            cart.clear()
            
            # Redirect to payment page
            return redirect('payment:payment_process', order_id=order.id)
    else:
        # Pre-fill form with user information if available
        initial_data = {}
        if request.user.first_name:
            initial_data['first_name'] = request.user.first_name
        if request.user.last_name:
            initial_data['last_name'] = request.user.last_name
        if request.user.email:
            initial_data['email'] = request.user.email
            
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'payment/checkout.html', {
        'form': form,
        'cart_products': cart_products,
        'total': total,
        'platform_cut': platform_cut,
        'grand_total': grand_total
    })

def payment_process(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'payment/payment.html', {
        'order': order
    })

def payment_success(request):
    return render(request, 'payment/success.html')

def payment_cancelled(request):
    return render(request, 'payment/cancelled.html')