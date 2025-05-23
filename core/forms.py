from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


INPUT_CLASSES = (
    'w-full py-4 px-6 rounded-xl '
    'bg-slate-800 border border-slate-700 '
    'text-gray-100 placeholder-gray-400 '
    'focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 '
    'transition duration-200'
)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASSES,
        'placeholder': 'Choose a username'
    }))   

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': INPUT_CLASSES,
        'placeholder': 'Enter your email'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': INPUT_CLASSES,
        'placeholder': 'Choose a password'
    }))  

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': INPUT_CLASSES,
        'placeholder': 'Confirm password'
    }))      

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASSES,
        'placeholder': 'Enter your username'
    }))   


    password = forms.CharField(widget=forms.PasswordInput(attrs=
                                                     {'class': INPUT_CLASSES, 
                                                      'placeholder': 'Enter your password'}))
    
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full border border-gray-300 rounded-lg p-2 text-black',
        'placeholder': 'Your name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full border border-gray-300 rounded-lg p-2 text-black',
        'placeholder': 'Your email'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full border border-gray-300 rounded-lg p-2 text-black resize-none',
        'placeholder': 'Your message',
        'rows': 4,
        'maxlength': 2000,
        'oninput': 'updateCharCount(this)'
    }))


class EditProfileForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'New password'
        })
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['new_password', 'confirm_password']:
                field.widget.attrs.update({
                    'class': INPUT_CLASSES,
                    'placeholder': f'Enter your {field.label.lower()}'
                })

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
