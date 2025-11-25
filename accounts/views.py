from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Address, OTPVerification
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .otp_utils import create_otp_record, send_otp_via_twilio, verify_otp
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Address 


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'customer')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('accounts:register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type=user_type
        )
        login(request, user)
        messages.success(request, 'Registration successful!')
        
        if user_type == 'vendor':
            return redirect('vendors:seller_registration_step1')
        return redirect('products:home')
    
    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('products:home')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('products:home')

@login_required
def profile(request):
    addresses = request.user.addresses.all()
    return render(request, 'accounts/profile.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        is_default = request.POST.get('is_default') == 'on'
        
        # If this is the first address or marked as default, set as default
        if is_default or not request.user.addresses.exists():
            request.user.addresses.all().update(is_default=False)
            is_default = True
        
        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            pincode=pincode,
            is_default=is_default
        )
        
        messages.success(request, 'Address added successfully!')
        return redirect('orders:checkout')
    
    return redirect('orders:checkout')
    
def add_address_page(request):
    return render(request, 'accounts/add_address_page.html')

def otp_login_request(request):
    """Request OTP for phone number"""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        
        if not phone:
            messages.error(request, 'Please enter a phone number')
            return render(request, 'accounts/otp_login_request.html')
        
        # Create OTP record
        otp_obj = create_otp_record(phone)
        
        # Send OTP via Twilio
        success, result = send_otp_via_twilio(phone, otp_obj.otp)
        
        if success:
            messages.success(request, 'OTP sent successfully! Check your phone.')
            request.session['otp_phone'] = phone
            return redirect('accounts:otp_verify')
        else:
            messages.error(request, f'Failed to send OTP: {result}')
    
    return render(request, 'accounts/otp_login_request.html')

def otp_verify(request):
    """Verify OTP and login user"""
    phone = request.session.get('otp_phone')
    
    if not phone:
        messages.error(request, 'Please request OTP first')
        return redirect('accounts:otp_login_request')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        
        success, message = verify_otp(phone, otp_code)
        
        if success:
            # Find or create user with this phone number
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                # Create new user
                username = f'user_{phone[-4:]}'
                user = User.objects.create_user(
                    username=username,
                    phone=phone,
                    password=User.objects.make_random_password()
                )
            
            login(request, user)
            messages.success(request, 'Login successful!')
            del request.session['otp_phone']
            return redirect('products:home')
        else:
            messages.error(request, message)
    
    return render(request, 'accounts/otp_verify.html', {'phone': phone})

def resend_otp(request):
    """Resend OTP to phone number"""
    phone = request.session.get('otp_phone')
    
    if not phone:
        messages.error(request, 'No phone number found')
        return redirect('accounts:otp_login_request')
    
    # Create new OTP
    otp_obj = create_otp_record(phone)
    success, result = send_otp_via_twilio(phone, otp_obj.otp)
    
    if success:
        messages.success(request, 'OTP resent successfully!')
    else:
        messages.error(request, f'Failed to resend OTP: {result}')
    
    return redirect('accounts:otp_verify')



@login_required
def edit_address(request, address_id):
    # Retrieve the address object, making sure it belongs to the current user
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    # You would typically use a Django form here, but for simplicity, we'll use POST data
    if request.method == 'POST':
        # Update the fields from the submitted form data
        address.full_name = request.POST.get('full_name')
        address.phone = request.POST.get('phone')
        address.address_line1 = request.POST.get('address_line1')
        address.address_line2 = request.POST.get('address_line2')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.pincode = request.POST.get('pincode')
        # Check if the 'is_default' checkbox was checked
        address.is_default = bool(request.POST.get('is_default')) 
        
        address.save()
        
        # Assuming 'orders:checkout' is the name of your checkout page URL
        return redirect('orders:checkout') 
        
    # Render the edit address form (you need to create this template)
    return render(request, 'accounts/edit_address_page.html', {'address': address})


@login_required
def delete_address(request, address_id):
    # Retrieve the address object, making sure it belongs to the current user
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    # Simple GET request deletion (safe only for internal links like on the checkout page)
    # A safer implementation would use POST for deletion
    if request.method == 'GET':
        address.delete()
        
    # Redirect back to the checkout page or the list of addresses
    # Assuming 'orders:checkout' is your target URL
    return redirect('orders:checkout')

# accounts/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def wishlist_view(request):
    # Logic to fetch and display the user's wishlist items
    context = {} # Populate context with wishlist data
    return render(request, 'accounts/wishlist.html', context)    