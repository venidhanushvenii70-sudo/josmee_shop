from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Address Management
    path('address/add/', views.add_address_page, name='add_address_page'),
    path('add-address/', views.add_address, name='add_address'),
    
    # 👇️ NEW ADDITIONS TO FIX THE NoReverseMatch ERROR
    path('address/edit/<int:address_id>/', views.edit_address, name='edit_address_page'),
    path('address/delete/<int:address_id>/', views.delete_address, name='delete_address'),
    # 👆️ NEW ADDITIONS TO FIX THE NoReverseMatch ERROR

    # OTP Authentication
    path('otp/request/', views.otp_login_request, name='otp_login_request'),
    path('otp/verify/', views.otp_verify, name='otp_verify'),
    path('otp/resend/', views.resend_otp, name='resend_otp'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]