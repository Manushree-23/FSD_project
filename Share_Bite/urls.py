from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-donation/', views.add_donation, name='add_donation'),
    path('request-donation/<int:donation_id>/', views.request_donation, name='request_donation'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('chat/<int:user_id>/', views.chat, name='chat'),


]
