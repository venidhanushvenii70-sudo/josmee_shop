from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vendor, SellerNotification
from products.models import Product, ProductImage, Category
from .forms import ProductForm, VendorProfileForm
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@login_required
def seller_registration_step1(request):
    """Step 1: Personal Information"""
    if request.user.user_type != 'vendor':
        messages.error(request, 'Only vendors can access seller registration')
        return redirect('products:home')
    
    if hasattr(request.user, 'vendor_profile'):
        return redirect('vendors:dashboard')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        email = request.POST.get('email', '').strip()
        
        if not all([full_name, contact_number, email]):
            messages.error(request, 'All fields are required')
            return render(request, 'vendors/seller_registration_step1.html')
        
        request.session['seller_step1'] = {
            'full_name': full_name,
            'contact_number': contact_number,
            'email': email,
        }
        return redirect('vendors:seller_registration_step2')
    
    return render(request, 'vendors/seller_registration_step1.html')

@login_required
def seller_registration_step2(request):
    """Step 2: Business Details"""
    if not request.session.get('seller_step1'):
        return redirect('vendors:seller_registration_step1')
    
    if request.method == 'POST':
        business_name = request.POST.get('business_name', '').strip()
        business_type = request.POST.get('business_type', '').strip()
        business_address = request.POST.get('business_address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        store_name = request.POST.get('store_name', '').strip()
        store_description = request.POST.get('store_description', '').strip()
        
        if not all([business_name, business_type, business_address, city, state, pincode, store_name, store_description]):
            messages.error(request, 'All fields are required')
            return render(request, 'vendors/seller_registration_step2.html')
        
        request.session['seller_step2'] = {
            'business_name': business_name,
            'business_type': business_type,
            'business_address': business_address,
            'city': city,
            'state': state,
            'pincode': pincode,
            'store_name': store_name,
            'store_description': store_description,
        }
        return redirect('vendors:seller_registration_step3')
    
    return render(request, 'vendors/seller_registration_step2.html')

@login_required
def seller_registration_step3(request):
    """Step 3: Tax Documents (PAN, GST)"""
    if not request.session.get('seller_step2'):
        return redirect('vendors:seller_registration_step2')
    
    if request.method == 'POST':
        pan_number = request.POST.get('pan_number', '').strip().upper()
        gst_number = request.POST.get('gst_number', '').strip().upper()
        
        if not pan_number:
            messages.error(request, 'PAN number is required')
            return render(request, 'vendors/seller_registration_step3.html')
        
        if len(pan_number) != 10:
            messages.error(request, 'Invalid PAN number format')
            return render(request, 'vendors/seller_registration_step3.html')
        
        request.session['seller_step3'] = {
            'pan_number': pan_number,
            'gst_number': gst_number,
        }
        
        if request.FILES.get('pan_card_image'):
            pan_file = request.FILES['pan_card_image']
            pan_path = default_storage.save(f'temp/vendor_docs/{request.user.id}/pan_{pan_file.name}', pan_file)
            request.session['pan_card_path'] = pan_path
            
        if request.FILES.get('gst_certificate'):
            gst_file = request.FILES['gst_certificate']
            gst_path = default_storage.save(f'temp/vendor_docs/{request.user.id}/gst_{gst_file.name}', gst_file)
            request.session['gst_certificate_path'] = gst_path
            
        return redirect('vendors:seller_registration_step4')
    
    return render(request, 'vendors/seller_registration_step3.html')

@login_required
def seller_registration_step4(request):
    """Step 4: Bank Details"""
    if not request.session.get('seller_step3'):
        return redirect('vendors:seller_registration_step3')
    
    if request.method == 'POST':
        bank_account_number = request.POST.get('bank_account_number', '').strip()
        bank_account_holder = request.POST.get('bank_account_holder', '').strip()
        bank_ifsc_code = request.POST.get('bank_ifsc_code', '').strip().upper()
        bank_name = request.POST.get('bank_name', '').strip()
        bank_branch = request.POST.get('bank_branch', '').strip()
        
        if not all([bank_account_number, bank_account_holder, bank_ifsc_code, bank_name, bank_branch]):
            messages.error(request, 'All bank details are required')
            return render(request, 'vendors/seller_registration_step4.html')
        
        # Combine all session data and create vendor profile
        step1 = request.session.get('seller_step1', {})
        step2 = request.session.get('seller_step2', {})
        step3 = request.session.get('seller_step3', {})
        
        vendor = Vendor.objects.create(
            user=request.user,
            full_name=step1['full_name'],
            contact_number=step1['contact_number'],
            email=step1['email'],
            business_name=step2['business_name'],
            business_type=step2['business_type'],
            business_address=step2['business_address'],
            city=step2['city'],
            state=step2['state'],
            pincode=step2['pincode'],
            store_name=step2['store_name'],
            store_description=step2['store_description'],
            pan_number=step3['pan_number'],
            gst_number=step3.get('gst_number', ''),
            bank_account_number=bank_account_number,
            bank_account_holder=bank_account_holder,
            bank_ifsc_code=bank_ifsc_code,
            bank_name=bank_name,
            bank_branch=bank_branch,
        )
        
        if 'pan_card_path' in request.session:
            pan_temp_path = request.session['pan_card_path']
            if default_storage.exists(pan_temp_path):
                # Read file content into memory and close file handle
                with default_storage.open(pan_temp_path, 'rb') as pan_file:
                    file_content = pan_file.read()
                    file_name = pan_temp_path.split('/')[-1]
                    vendor.pan_card_image.save(file_name, ContentFile(file_content), save=False)
                # Now file handle is closed, safe to delete
                default_storage.delete(pan_temp_path)
        
        if 'gst_certificate_path' in request.session:
            gst_temp_path = request.session['gst_certificate_path']
            if default_storage.exists(gst_temp_path):
                # Read file content into memory and close file handle
                with default_storage.open(gst_temp_path, 'rb') as gst_file:
                    file_content = gst_file.read()
                    file_name = gst_temp_path.split('/')[-1]
                    vendor.gst_certificate.save(file_name, ContentFile(file_content), save=False)
                # Now file handle is closed, safe to delete
                default_storage.delete(gst_temp_path)
        
        # Handle bank proof upload from step 4
        if request.FILES.get('bank_proof'):
            vendor.bank_proof = request.FILES['bank_proof']
        
        vendor.save()
        
        SellerNotification.objects.create(
            vendor=vendor,
            title='Welcome to Josmee Seller Platform!',
            message=f'Congratulations {vendor.full_name}! Your seller account has been created. Your documents are under verification. You will be notified once approved.'
        )
        
        # Clear session data
        for key in ['seller_step1', 'seller_step2', 'seller_step3', 'pan_card_path', 'gst_certificate_path']:
            if key in request.session:
                del request.session[key]
        
        messages.success(request, 'Seller registration completed! Your documents are under verification.')
        return redirect('vendors:dashboard')
    
    return render(request, 'vendors/seller_registration_step4.html')

@login_required
def setup_store(request):
    if request.user.user_type != 'vendor':
        messages.error(request, 'Only vendors can set up stores')
        return redirect('products:home')
    
    if hasattr(request.user, 'vendor_profile'):
        return redirect('vendors:dashboard')
    
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        store_description = request.POST.get('store_description')
        
        Vendor.objects.create(
            user=request.user,
            store_name=store_name,
            store_description=store_description
        )
        messages.success(request, 'Store created successfully!')
        return redirect('vendors:dashboard')
    
    return render(request, 'vendors/setup_store.html')

@login_required
def vendor_dashboard(request):
    if not hasattr(request.user, 'vendor_profile'):
        return redirect('vendors:seller_registration_step1')
    
    vendor = request.user.vendor_profile
    products = vendor.products.all()
    notifications = vendor.notifications.all()[:5]  # Get latest 5 notifications
    
    total_products = products.count()
    active_products = products.filter(stock__gt=0).count()
    total_orders = vendor.orders.count()
    pending_orders = vendor.orders.filter(status='pending').count()
    
    return render(request, 'vendors/dashboard.html', {
        'vendor': vendor,
        'products': products,
        'notifications': notifications,
        'total_products': total_products,
        'active_products': active_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
    })

@login_required
def add_product(request):
    if not hasattr(request.user, 'vendor_profile'):
        messages.error(request, 'Please complete seller registration first')
        return redirect('vendors:seller_registration_step1')
    
    vendor = request.user.vendor_profile
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.slug = slugify(f"{product.name}-{vendor.id}")
            product.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for index, image in enumerate(images):
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_primary=(index == 0)
                )
            
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('vendors:dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'vendors/add_product.html', {'form': form})

@login_required
def edit_profile(request):
    if not hasattr(request.user, 'vendor_profile'):
        return redirect('vendors:setup_store')
        
    vendor = request.user.vendor_profile
    
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('vendors:dashboard')
    else:
        form = VendorProfileForm(instance=vendor)
        
    return render(request, 'vendors/edit_profile.html', {'form': form})

def become_supplier(request):
    """Landing page for prospective suppliers"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'vendor_profile'):
            return redirect('vendors:dashboard')
        elif request.user.user_type == 'vendor':
            return redirect('vendors:seller_registration_step1')
    
    return render(request, 'vendors/become_supplier.html')
