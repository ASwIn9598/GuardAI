from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Use your custom User model

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")