from django import forms
from .models import Item
INPUT_CLASSES = 'w-full py-3 px-4 rounded-xl border border-gray-300 focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-200 transition duration-200'
class NewItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields = ( 'Category','name','description','price','image')

        widgets = {
            'Category': forms.Select(attrs={
                'class':INPUT_CLASSES,

                }),    
            'name': forms.TextInput(attrs={
                'class':INPUT_CLASSES,

                }),
            'description': forms.Textarea(attrs={
                'class':INPUT_CLASSES,
            }),
            'price': forms.TextInput(attrs={
                'class':INPUT_CLASSES,

                })   ,
            'image': forms.FileInput(attrs={
                'class':INPUT_CLASSES,

                })    
        }  
        

class EditItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields = ( 'name','description','price','image','is_sold')

        widgets = {
                
            'name': forms.TextInput(attrs={
                'class':INPUT_CLASSES,

                }),
            'description': forms.Textarea(attrs={
                'class':INPUT_CLASSES,
            }),
            'price': forms.TextInput(attrs={
                'class':INPUT_CLASSES,

                })   ,
            'image': forms.FileInput(attrs={
                'class':INPUT_CLASSES,

                })    
        }
