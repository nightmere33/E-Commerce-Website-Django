from django.shortcuts import render,redirect
from item.models import Category,Item
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import EditProfileForm
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

def index(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')[:6]  # Retour à 6 items
    categories = Category.objects.all()
    
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been sent!")
            return redirect('contact')
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