from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from decimal import Decimal

@login_required
def checkout(request):
    # Récupérer la méthode de paiement choisie
    payment_method = request.GET.get('payment_method', 'credit_card')
    
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
            
            # Définir des valeurs par défaut pour les champs retirés
            order.address = "Digital Purchase - No Address Required"
            order.postal_code = "00000"
            order.city = "Digital"
            
            order.save()
            
            # Create order items
            for product in cart_products:
                OrderItem.objects.create(
                    order=order,
                    product_id=product.id,
                    price=product.price,
                    quantity=product.quantity
                )
            
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
        'grand_total': grand_total,
        'payment_method': payment_method  # Passer la méthode de paiement au template
    })

def payment_process(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'payment/payment.html', {
        'order': order
    })

@login_required
def payment_success(request):
    # Récupère la dernière commande de l'utilisateur
    order = Order.objects.filter(user=request.user).order_by('-created').first()
    
    if order:
        # Prépare le contenu de l'email
        subject = f"Your GameVerse Order #{order.id} Confirmation"
        
        # Version HTML de l'email
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #2dd4bf; color: white; padding: 10px 20px; border-radius: 5px; }}
        .footer {{ font-size: 12px; color: #888; margin-top: 30px; }}
        .game-key {{ background-color: #f0f0f0; padding: 5px; border-radius: 3px; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Thank You for Your Purchase!</h2>
        </div>
        <p>Hello {order.first_name},</p>
        <p>We're excited to confirm your recent purchase on GameVerse.</p>
        
        <h3>Order Details:</h3>
        <p>
            <strong>Order Number:</strong> #{order.id}<br>
            <strong>Date:</strong> {order.created.strftime('%B %d, %Y')}<br>
            <strong>Total Amount:</strong> ${order.total_paid}
        </p>
        
        <h3>Your Game Keys:</h3>
        <ul>
"""
        
        # Texte brut pour les clients qui ne lisent pas le HTML
        text_message = f"""
Hello {order.first_name},

Thank you for your purchase on GameVerse!

ORDER DETAILS
-------------
Order Number: #{order.id}
Date: {order.created.strftime('%B %d, %Y')}
Total Amount: ${order.total_paid}

YOUR GAME KEYS
--------------
"""
        
        # Ajoute les clés de jeu pour chaque produit acheté
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            # Trouver le nom du produit de façon sécurisée
            try:
                product_name = item.product.name
            except AttributeError:
                try:
                    product_name = item.item.name
                except AttributeError:
                    try:
                        product_name = item.name
                    except AttributeError:
                        product_name = f"Game Item {item.id}"
            
            game_key = "XXXX-XXXX-XXXX-XXXX"  # Générer une vraie clé
            
            # Ajouter au message HTML
            html_message += f'<li><strong>{product_name}:</strong> <span class="game-key">{game_key}</span></li>\n'
            
            # Ajouter au message texte
            text_message += f"{product_name}: {game_key}\n"
        
        # Fermer la liste et ajouter les instructions
        html_message += """
        </ul>
        
        <h3>Instructions:</h3>
        <ol>
            <li>Download the game client from the official website</li>
            <li>Install the game and launch it</li>
            <li>Enter your key when prompted</li>
        </ol>
        
        <p>If you encounter any issues, please contact our support team.</p>
        
        <p>Thank you for choosing GameVerse!</p>
        
        <p>Best regards,<br>
        The GameVerse Team</p>
        
        <div class="footer">
            <p>This email was sent to you as a registered user of GameVerse. 
            To ensure our emails reach your inbox, please add gameversesuppdz@gmail.com to your contacts.</p>
            <p>© 2025 GameVerse. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Compléter le message texte
        text_message += """
INSTRUCTIONS
------------
1. Download the game client from the official website
2. Install the game and launch it
3. Enter your key when prompted

If you encounter any issues, please contact our support team.

Thank you for choosing GameVerse!

Best regards,
The GameVerse Team

---
To ensure our emails reach your inbox, please add gameversesuppdz@gmail.com to your contacts.
© 2025 GameVerse. All rights reserved.
"""
        
        # Envoie l'email
        try:
            send_mail(
                subject,
                text_message,  # Version texte
                'GameVerse <gameversesuppdz@gmail.com>',  # Format avec nom d'expéditeur
                [order.email],
                fail_silently=False,
                html_message=html_message  # Version HTML
            )
            messages.success(request, "Thank you for your purchase! A confirmation email with your game keys has been sent to your email address.")
        except Exception as e:
            messages.error(request, f"Your payment was successful, but we couldn't send the confirmation email. Please contact support.")
    
    # Vider le panier ici, après le paiement réussi
    cart = Cart(request)
    cart.clear()
    
    return render(request, 'payment/success.html')

def payment_cancelled(request):
    return render(request, 'payment/cancelled.html')