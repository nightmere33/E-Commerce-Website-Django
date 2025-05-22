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