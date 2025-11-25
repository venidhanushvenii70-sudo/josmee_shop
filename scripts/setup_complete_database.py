"""Complete database setup script for Josmee Online Shopping"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'josmee_projects.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, HeroSlider, Product, ProductImage
from vendors.models import Vendor
from accounts.models import OTPVerification

User = get_user_model()

def setup_database():
    print("🚀 Setting up Josmee Online Shopping Database...")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@josmee.com',
            password='admin123'
        )
        print("✅ Admin user created (username: admin, password: admin123)")
    
    # Create sample categories
    categories_data = [
        {'name': 'Fashion', 'slug': 'fashion', 'icon': 'fas fa-tshirt', 'description': 'Trendy clothing and accessories'},
        {'name': 'Electronics', 'slug': 'electronics', 'icon': 'fas fa-laptop', 'description': 'Latest gadgets and electronics'},
        {'name': 'Home & Living', 'slug': 'home-living', 'icon': 'fas fa-home', 'description': 'Home decor and essentials'},
        {'name': 'Beauty', 'slug': 'beauty', 'icon': 'fas fa-spa', 'description': 'Beauty and personal care'},
        {'name': 'Books', 'slug': 'books', 'icon': 'fas fa-book', 'description': 'Books and stationery'},
        {'name': 'Sports', 'slug': 'sports', 'icon': 'fas fa-running', 'description': 'Sports and fitness gear'},
        {'name': 'Toys', 'slug': 'toys', 'icon': 'fas fa-gamepad', 'description': 'Toys and games'},
        {'name': 'Jewelry', 'slug': 'jewelry', 'icon': 'fas fa-gem', 'description': 'Jewelry and accessories'},
    ]
    
    for cat_data in categories_data:
        Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
    print(f"✅ Created {len(categories_data)} categories")
    
    # Create hero sliders
    if not HeroSlider.objects.exists():
        HeroSlider.objects.create(
            title="Welcome to Josmee Online Shopping",
            subtitle="Discover Amazing Products from Thousands of Verified Sellers",
            button_text="Start Shopping",
            button_link="/products/",
            is_active=True,
            order=1
        )
        HeroSlider.objects.create(
            title="Become a Seller Today",
            subtitle="Join thousands of successful sellers and grow your business",
            button_text="Sell on Josmee",
            button_link="/accounts/register/",
            is_active=True,
            order=2
        )
        print("✅ Created hero sliders")
    
    # Create sample vendor
    if not User.objects.filter(username='vendor1').exists():
        vendor_user = User.objects.create_user(
            username='vendor1',
            email='vendor@josmee.com',
            password='vendor123',
            user_type='vendor'
        )
        
        Vendor.objects.create(
            user=vendor_user,
            store_name='Premium Store',
            store_description='Quality products at best prices',
            full_name='John Seller',
            contact_number='9876543210',
            email='vendor@josmee.com',
            is_verified=True,
            verification_status='approved'
        )
        print("✅ Sample vendor created (username: vendor1, password: vendor123)")
    
    print("\n🎉 Database setup complete!")
    print("\n📋 Next Steps:")
    print("1. Run: python manage.py migrate")
    print("2. Run: python manage.py runserver")
    print("3. Visit: http://127.0.0.1:8000")
    print("4. Admin Panel: http://127.0.0.1:8000/admin")
    print("5. Add products from vendor dashboard")
    print("\n💡 Test OTP: Check console for OTP codes when testing login")

if __name__ == '__main__':
    setup_database()
