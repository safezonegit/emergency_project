from django import forms
from .models import CustomUserModel
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUserModel
        fields = ['email', 'phone_number', 'password1', 'password2']