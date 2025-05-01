from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Donation

class UserRegisterForm(UserCreationForm):
    is_donator = forms.BooleanField(required=False, label="Register as Donator")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_donator']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['category', 'description', 'quantity', 'location']