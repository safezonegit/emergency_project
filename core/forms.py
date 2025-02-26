from django import forms
from .models import AnonymousResponse

class AnonymousResponseForm(forms.ModelForm):
    class Meta:
        model = AnonymousResponse
        fields = ['phone_number', 'message']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number - (optional)'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Message',
                'class': 'message_input'
            }),
        }
