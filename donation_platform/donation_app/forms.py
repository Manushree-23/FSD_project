from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Donation
from django.utils import timezone
import datetime

class UserRegisterForm(UserCreationForm):
    is_donator = forms.BooleanField(required=False, label="Register as Donator")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_donator']

class DonationForm(forms.ModelForm):
    today = timezone.now().date()
    max_date = today + datetime.timedelta(days=5)

    HOUR_CHOICES = [(str(i), str(i)) for i in range(1, 13)]
    MINUTE_CHOICES = [(f'{i:02}', f'{i:02}') for i in range(0, 60, 5)]
    AM_PM_CHOICES = [('AM', 'AM'), ('PM', 'PM')]

    pickup_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': today.strftime('%Y-%m-%d'),
                'max': max_date.strftime('%Y-%m-%d'),
            }
        ),
        required=False,
    )

    pickup_hour = forms.ChoiceField(choices=HOUR_CHOICES, required=False)
    pickup_minute = forms.ChoiceField(choices=MINUTE_CHOICES, required=False)
    pickup_am_pm = forms.ChoiceField(choices=AM_PM_CHOICES, required=False)

    class Meta:
        model = Donation
        fields = ['category', 'description', 'quantity', 'location', 'pickup_date']

    def clean(self):
        cleaned_data = super().clean()

        category = cleaned_data.get('category')
        pickup_date = cleaned_data.get('pickup_date')

        if pickup_date:
            if category == 'food' and pickup_date != self.today:
                self.add_error('pickup_date', 'For food donations, pickup date must be today.')
            elif category == 'clothes' and (pickup_date < self.today or pickup_date > self.max_date):
                self.add_error('pickup_date', f'For clothes donations, pickup date must be between today and {self.max_date}.')

        hour = cleaned_data.get('pickup_hour')
        minute = cleaned_data.get('pickup_minute')
        am_pm = cleaned_data.get('pickup_am_pm')

        if hour and minute and am_pm:
            hour = int(hour)
            minute = int(minute)
            if am_pm == 'PM' and hour != 12:
                hour += 12
            elif am_pm == 'AM' and hour == 12:
                hour = 0
            cleaned_data['pickup_time'] = datetime.time(hour, minute)
        else:
            cleaned_data['pickup_time'] = None

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.pickup_time = self.cleaned_data.get('pickup_time')
        if commit:
            instance.save()
        return instance