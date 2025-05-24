from django.contrib import admin
from .models import Donation, Request, Profile, Message

admin.site.register(Donation)
admin.site.register(Request)
admin.site.register(Profile)
admin.site.register(Message)

# Register your models here.
