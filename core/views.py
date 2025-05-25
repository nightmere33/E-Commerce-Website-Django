from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import EditProfileForm
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.conf import settings  
from django.core.mail import send_mail
import random
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from langdetect import detect

def index(request):
    # Get all categories
    categories = Category.objects.all()
    
    # Get all items except gift cards - CORRECTED LINE
    all_items = Item.objects.filter(is_sold=False).exclude(Category__name__icontains="gift")
    
    # Get newest items for the "Newest Games" section
    newest_items = all_items.order_by('-created_at')[:15]
    
    # Get random items for the carousel (different from newest items)
    # Convert QuerySet to list to use random.sample
    all_items_list = list(all_items)
    # Make sure we have enough items for the carousel
    carousel_count = min(10, len(all_items_list))
    # Select random items
    random_carousel_items = random.sample(all_items_list, carousel_count)
    
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': newest_items,  # For "Newest Games" section
        'carousel_items': random_carousel_items  # For the carousel
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Contenu de l’e-mail
            subject = f"New Contact Message from {name}"
            message_body = f"From: {name} <{email}>\n\nMessage:\n{message}"

            # Envoi de l’e-mail
            send_mail(
                subject,
                message_body,
                'gameversesuppdz@gmail.com',       
                ['gameversesuppdz@gmail.com'],  
                fail_silently=False,
            )

            messages.success(request, 'Message sent successfully!')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:

        form = SignUpForm()

    return render(request, 'core/signup.html', {
        'form': form,
    })


def privacy(request):
    return render(request, 'core/privacy.html')

def termsofuse(request):
    return render(request, 'core/termsofuse.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if new_password:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    update_session_auth_hash(request, user)  # évite la déconnexion
                    messages.success(request, 'Password updated successfully.')
                else:
                    messages.error(request, 'Passwords do not match.')
                    return redirect('core:edit_profile')

            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('core:edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'core/edit_profile.html', {
        'form': form,
    })


#chatbot AI

API_KEY = settings.OPENROUTER_API_KEY

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are VerseBot, the intelligent assistant of the GameVerse website.\n"
                        "First, detect the user's language (French or English) based on the message.\n"
                        "Then, always respond in the same language the user used.\n\n"

                        "If the question is about how to use the GameVerse website (e.g., login, sign up, search games, add to cart, see invoice, pay, contact admin), "
                        "give a clear, helpful, and simple answer.\n\n"

                        "Examples:\n"
                        "- FR : Comment puis-je me connecter ?\n"
                        "- EN : How can I log in?\n"
                        "- FR : Où puis-je créer un compte ?\n"
                        "- EN : How to create an account?\n"
                        "- FR : Comment rechercher un jeu ?\n"
                        "- EN : How can I search for a game?\n"
                        "- FR : Comment ajouter un jeu au panier ?\n"
                        "- EN : How to add a game to the cart?\n"
                        "- FR : Où voir ma facture ?\n"
                        "- EN : Where can I see my invoice?\n"
                        "- FR : Comment payer mes jeux ?\n"
                        "- EN : How to pay for my games?\n"
                        "- FR : Comment contacter l’administrateur ?\n"
                        "- EN : How to contact the administrator?\n\n"

                        "If the user asks something else, respond like a helpful assistant.\n"
                        "Never mix languages in your answer. Always match the language of the user's question."
                    )

                },
                {"role": "user", "content": user_input}
        ]
    }

        try:

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=20
            )
            result = response.json()

            if "choices" in result:
                reply = result["choices"][0]["message"]["content"]
                return JsonResponse({"reply": reply})
            else:
                print("Erreur dans la réponse OpenRouter :", result)
                return JsonResponse({"reply": "Une erreur est survenue. Vérifie ta clé ou ton quota OpenRouter."}, status=500)
        
        except Exception as e:
            print("Erreur chatbot :", str(e))
            return JsonResponse({"reply": "Une erreur de communication avec le serveur est survenue."}, status=500)
