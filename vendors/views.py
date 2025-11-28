from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from orders.models import Order, OrderItem
from .models import Vendor, SellerNotification
from .forms import ProductForm, VendorProfileForm
from products.models import Product, ProductImage, Category


# -------------------- Seller Registration Steps --------------------

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
                with default_storage.open(pan_temp_path, 'rb') as pan_file:
                    vendor.pan_card_image.save(pan_temp_path.split('/')[-1], ContentFile(pan_file.read()), save=False)
                default_storage.delete(pan_temp_path)

        if 'gst_certificate_path' in request.session:
            gst_temp_path = request.session['gst_certificate_path']
            if default_storage.exists(gst_temp_path):
                with default_storage.open(gst_temp_path, 'rb') as gst_file:
                    vendor.gst_certificate.save(gst_temp_path.split('/')[-1], ContentFile(gst_file.read()), save=False)
                default_storage.delete(gst_temp_path)

        if request.FILES.get('bank_proof'):
            vendor.bank_proof = request.FILES['bank_proof']

        vendor.save()

        SellerNotification.objects.create(
            vendor=vendor,
            title='Welcome to Josmee Seller Platform!',
            message=f'Congratulations {vendor.full_name}! Your seller account has been created. Documents under verification.'
        )

        for key in ['seller_step1', 'seller_step2', 'seller_step3', 'pan_card_path', 'gst_certificate_path']:
            request.session.pop(key, None)

        messages.success(request, 'Seller registration completed! Your documents are under verification.')
        return redirect('vendors:dashboard')

    return render(request, 'vendors/seller_registration_step4.html')


# -------------------- Store Setup --------------------

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
        Vendor.objects.create(user=request.user, store_name=store_name, store_description=store_description)
        messages.success(request, 'Store created successfully!')
        return redirect('vendors:dashboard')

    return render(request, 'vendors/setup_store.html')


# -------------------- Vendor Dashboard --------------------

@login_required
def vendor_dashboard(request):
    """Seller Dashboard with orders, products, notifications"""
    if not hasattr(request.user, 'vendor_profile'):
        return redirect('vendors:seller_registration_step1')

    vendor = request.user.vendor_profile

    # Vendor products
    vendor_products = Product.objects.filter(vendor=vendor)

    # Vendor orders
    vendor_items = OrderItem.objects.filter(product__in=vendor_products)
    vendor_order_ids = vendor_items.values_list('order_id', flat=True).distinct()
    vendor_orders = Order.objects.filter(id__in=vendor_order_ids).order_by("-created_at")

    # Stats
    total_orders = vendor_orders.count()
    pending_orders = vendor_orders.filter(status='pending').count()
    confirmed_orders = vendor_orders.filter(status='confirmed').count()
    shipped_orders = vendor_orders.filter(status='shipped').count()
    delivered_orders = vendor_orders.filter(status='delivered').count()
    cancelled_orders = vendor_orders.filter(status='cancelled').count()

    # Notifications
    notifications = vendor.notifications.all()[:5] if hasattr(vendor, 'notifications') else []

    return render(request, 'vendors/dashboard.html', {
        "vendor": vendor,
        "products": vendor_products,
        "notifications": notifications,
        "orders": vendor_orders,
        "order_items": vendor_items,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "confirmed_orders": confirmed_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
    })


# -------------------- Product Management --------------------

@login_required
def add_product(request):
    if not hasattr(request.user, 'vendor_profile'):
        messages.error(request, 'Please complete seller registration first')
        return redirect('vendors:seller_registration_step1')

    vendor = request.user.vendor_profile
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price') or 0
        stock = request.POST.get('stock')
        images = request.FILES.getlist('images')

        if not all([name, description, category_id, price, stock]) or not images:
            messages.error(request, 'Please fill all required fields and upload at least one image.')
            return render(request, 'vendors/add_product.html', {'categories': categories})

        product = Product.objects.create(
            vendor=vendor,
            name=name,
            description=description,
            category_id=category_id,
            price=price,
            discount_price=discount_price,
            stock=stock,
            slug=slugify(f"{name}-{vendor.id}"),
            is_active=True
        )

        for idx, image in enumerate(images):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(idx == 0)
            )

        SellerNotification.objects.create(
            vendor=vendor,
            title=f'Product "{product.name}" Added',
            message=f'Your product "{product.name}" has been successfully added.'
        )

        messages.success(request, f'Product "{product.name}" added successfully!')
        return redirect('vendors:dashboard')

    return render(request, 'vendors/add_product.html', {'categories': categories})


@login_required
def edit_product(request, product_id):
    if not hasattr(request.user, 'vendor_profile'):
        messages.error(request, 'Please complete seller registration first')
        return redirect('vendors:seller_registration_step1')

    vendor = request.user.vendor_profile
    product = get_object_or_404(Product, id=product_id, vendor=vendor)
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price') or 0
        stock = request.POST.get('stock')
        images = request.FILES.getlist('images')

        if not all([name, description, category_id, price, stock]):
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'vendors/edit_product.html', {'product': product, 'categories': categories})

        product.name = name
        product.description = description
        product.category_id = category_id
        product.price = price
        product.discount_price = discount_price
        product.stock = stock
        product.slug = slugify(f"{name}-{vendor.id}")
        product.save()

        if images:
            product.images.all().delete()
            for idx, image in enumerate(images):
                ProductImage.objects.create(product=product, image=image, is_primary=(idx == 0))

        SellerNotification.objects.create(
            vendor=vendor,
            title=f'Product "{product.name}" Updated',
            message=f'Your product "{product.name}" has been successfully updated.'
        )

        messages.success(request, f'Product "{product.name}" updated successfully!')
        return redirect('vendors:dashboard')

    return render(request, 'vendors/edit_product.html', {'product': product, 'categories': categories})


@login_required
def delete_product(request, product_id):
    if not hasattr(request.user, 'vendor_profile'):
        messages.error(request, 'Please complete seller registration first')
        return redirect('vendors:seller_registration_step1')

    product = get_object_or_404(Product, id=product_id, vendor=request.user.vendor_profile)

    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product "{product.name}" deleted successfully!')
        return redirect('vendors:dashboard')

    return render(request, 'vendors/confirm_delete_product.html', {'product': product})


# -------------------- Vendor Profile --------------------

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


# -------------------- Become Supplier Landing --------------------

def become_supplier(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'vendor_profile'):
            return redirect('vendors:dashboard')
        elif request.user.user_type == 'vendor':
            return redirect('vendors:seller_registration_step1')

    return render(request, 'vendors/become_supplier.html')


# -------------------- Update Order Status --------------------

@login_required
def update_order_status(request, order_id, status):
    if not hasattr(request.user, 'vendor_profile'):
        return redirect('vendors:seller_registration_step1')

    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()

    messages.success(request, f"Order {order.order_number} updated to {status.upper()}!")
    return redirect('vendors:dashboard')
