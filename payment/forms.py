from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg bg-slate-800 text-gray-100 border-slate-700 focus:outline-none focus:ring-2 focus:ring-teal-400'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg bg-slate-800 text-gray-100 border-slate-700 focus:outline-none focus:ring-2 focus:ring-teal-400'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded-lg bg-slate-800 text-gray-100 border-slate-700 focus:outline-none focus:ring-2 focus:ring-teal-400'}),
        }