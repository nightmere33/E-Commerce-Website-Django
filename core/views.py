from django.shortcuts import render,redirect
from item.models import Category,Item
from .forms import SignUpForm
# Create your views here.
from .forms import ContactForm
from django.contrib import messages

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html',{
        'categories':categories,
        'items':items,
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Ici tu peux traiter les données : les enregistrer ou envoyer un email
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