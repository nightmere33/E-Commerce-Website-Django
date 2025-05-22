from django import forms
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border border-gray-300 text-gray-900 focus:outline-none focus:ring-2 focus:ring-teal-500 resize-none',
                'placeholder': 'Type your message here...',
                'maxlength': '2000',
                'rows': 5,
            }),
        }





# from django import forms
# from .models import Conversation, ConversationMessage

# class ConversationMessageForm(forms.ModelForm):
#     class Meta:
#         model = ConversationMessage
#         fields = ['content']
#         widgets = {
#             'content': forms.Textarea(attrs={'class':'w-full py-4 px-6 rounded-xl border'}),
#         }