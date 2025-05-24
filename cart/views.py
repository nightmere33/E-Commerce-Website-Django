from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from item.models import Item
from conversation.forms import ConversationMessageForm
from conversation.models import Conversation
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone

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
    if request.POST.get('action') == 'post':
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
        response = JsonResponse({'qty': cart_quantity})
        return response

@require_POST
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        #return redirect('cart_summary')
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response

def cart_update(request):
    pass

@login_required
def baridimob_redirect(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    
    if not cart_products:
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_summary')
    
    # Récupérer l'administrateur (supposons que l'ID 1 est l'administrateur)
    from django.contrib.auth.models import User
    try:
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            # Si aucun superutilisateur n'est trouvé, utilisez le premier utilisateur staff
            admin = User.objects.filter(is_staff=True).first()
            if not admin:
                messages.error(request, "Sorry, we couldn't process your BaridiMob payment request at this time. Please try again later.")
                return redirect('cart:cart_summary')
    except Exception as e:
        messages.error(request, "An error occurred. Please try again later.")
        return redirect('cart:cart_summary')
    
    # Utiliser le premier produit pour la conversation
    first_product = cart_products[0]
    
    # Vérifier si une conversation existe déjà entre l'acheteur et l'administrateur
    conversations = Conversation.objects.filter(
        item=first_product,
        members=request.user
    ).filter(
        members=admin
    )
    
    # Préparer le reçu détaillé avec un formatage simple mais efficace
    cart_content = "\n".join([f"• {p.name} x{p.quantity}: ${float(p.price) * p.quantity:.2f}" for p in cart_products])
    total = sum(float(p.price) * p.quantity for p in cart_products)
    platform_cut = round(total * 0.05, 2)
    grand_total = round(total + platform_cut, 2)
    
    # Créer un nom d'utilisateur propre pour l'affichage
    display_name = f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username
    
    # Utiliser un format de texte simple mais bien structuré
    receipt_message = f"""===== BARIDIMOB PAYMENT REQUEST =====

CUSTOMER INFORMATION:
• Name: {display_name}
• Username: {request.user.username}
• Email: {request.user.email}
• Date: {timezone.now().strftime('%B %d, %Y %H:%M')}

ORDER DETAILS:
{cart_content}

PAYMENT SUMMARY:
• Subtotal: ${total:.2f}
• Platform Fee (5%): ${platform_cut:.2f}
• Total: ${grand_total:.2f}

------------------------------------------

I would like to purchase these games using BaridiMob payment method.
Please provide me with the necessary payment instructions to complete this transaction.

Thank you for your assistance
"""

    if conversations.exists():
        conversation = conversations.first()
        
        # Créer directement le message dans la conversation existante
        from conversation.models import ConversationMessage
        
        ConversationMessage.objects.create(
            conversation=conversation,
            content=receipt_message,
            created_by=request.user
        )
        
        messages.success(request, "Your BaridiMob payment request has been sent to the administrator. Please check your messages for payment instructions.")
    else:
        # Créer une nouvelle conversation
        conversation = Conversation.objects.create(item=first_product)
        conversation.members.add(request.user)
        conversation.members.add(admin)
        
        # Créer directement le message dans la nouvelle conversation
        from conversation.models import ConversationMessage
        
        ConversationMessage.objects.create(
            conversation=conversation,
            content=receipt_message,
            created_by=request.user
        )
        
        messages.success(request, "Your BaridiMob payment request has been sent to the administrator. Please check your messages for payment instructions.")
    
    # Vider le panier après avoir envoyé le message
    cart.clear()
    
    return redirect('conversation:detail', pk=conversation.id)