from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_donator = models.BooleanField(default=False)

class Donation(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('clothes', 'Clothes'),
    ]

    donator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField()
    quantity = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Request(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    ngo = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
