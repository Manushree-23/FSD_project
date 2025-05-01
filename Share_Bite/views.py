from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import UserRegisterForm, DonationForm
from .models import Donation, Request
from django.contrib.auth.models import User
from .models import Profile,Message
from django.db.models import Q



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure profile is created even if signals didn't fire
            profile, created = Profile.objects.get_or_create(user=user)
            profile.is_donator = form.cleaned_data['is_donator']
            profile.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Automatically create profile if missing
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.user.is_superuser:
        donations = Donation.objects.all()
        return render(request, 'dashboard_ngo.html', {'donations': donations , 'user': request.user})
    elif profile.is_donator:
        donations = Donation.objects.filter(donator=request.user)
        return render(request, 'dashboard_donator.html', {'donations': donations})
    else:
        donations = Donation.objects.all()
        return render(request, 'dashboard_ngo.html', {'donations': donations , 'user': request.user})


@login_required
def add_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donator = request.user
            donation.save()
            return redirect('dashboard')
    else:
        form = DonationForm()
    return render(request, 'donation_form.html', {'form': form})


@login_required
def request_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    Request.objects.create(donation=donation, ngo=request.user)
    donation.available = False
    donation.save()
    send_mail(
        'Your donation has been requested!',
        f'{request.user.username} has requested your donation: {donation.description}',
        'noreply@example.com',
        [donation.donator.email],
    )
    return redirect('dashboard')


@login_required
def accept_request(request, request_id):
    donation_request = get_object_or_404(Request, id=request_id, donation__donator=request.user)
    donation_request.accepted = True
    donation_request.save()
    return redirect('dashboard')

@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Allow chat if there's any accepted request between these two users
    has_accepted_request = Request.objects.filter(
        (
            Q(ngo=other_user, donation__donator=request.user) |
            Q(ngo=request.user, donation__donator=other_user)
        ) & Q(accepted=True)
    ).exists()

    if not has_accepted_request:
        return redirect('dashboard')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    )

    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages
    })
