from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from products.models import Category, Product, Brand, HeroSlider
from vendors.models import Vendor
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Superuser/Vendor if not exists
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'user_type': 'vendor'
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (password: admin123)'))

        # Create Vendor Profile
        vendor, created = Vendor.objects.get_or_create(
            user=user,
            defaults={
                'full_name': 'Josmee Official',
                'contact_number': '9876543210',
                'email': 'admin@example.com',
                'business_name': 'Josmee Retail',
                'store_name': 'Josmee Official Store',
                'business_address': '123 Main St',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400001',
                'bank_account_number': '1234567890',
                'bank_account_holder': 'Josmee Retail',
                'bank_ifsc_code': 'SBIN0001234',
                'bank_name': 'SBI',
                'bank_branch': 'Main Branch',
            }
        )

        # 2. Create Categories
        categories_data = [
            {'name': 'Women Fashion', 'icon': 'fas fa-female'},
            {'name': 'Men Fashion', 'icon': 'fas fa-male'},
            {'name': 'Electronics', 'icon': 'fas fa-mobile-alt'},
            {'name': 'Home & Kitchen', 'icon': 'fas fa-couch'},
            {'name': 'Beauty & Health', 'icon': 'fas fa-heart'},
            {'name': 'Jewellery', 'icon': 'fas fa-gem'},
            {'name': 'Bags & Footwear', 'icon': 'fas fa-shopping-bag'},
            {'name': 'Kids', 'icon': 'fas fa-child'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, _ = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'icon': cat_data['icon']
                }
            )
            categories[cat_data['name']] = category

        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))

        # 3. Create Brands
        brands_data = ['Nike', 'Adidas', 'Samsung', 'Apple', 'Zara', 'H&M', 'Puma', 'Levis']
        brands = []
        for name in brands_data:
            brand, _ = Brand.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'is_featured': True
                }
            )
            brands.append(brand)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(brands)} brands'))

        # 4. Create Hero Sliders
        sliders_data = [
            {
                'title': 'Big Sale on Fashion',
                'subtitle': 'Get up to 70% off on top brands',
                'button_text': 'Shop Now',
            },
            {
                'title': 'New Electronics',
                'subtitle': 'Latest gadgets at unbeatable prices',
                'button_text': 'Explore',
            }
        ]
        
        for i, slider in enumerate(sliders_data):
            HeroSlider.objects.get_or_create(
                title=slider['title'],
                defaults={
                    'subtitle': slider['subtitle'],
                    'button_text': slider['button_text'],
                    'order': i
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Created hero sliders'))

        # 5. Create Products
        if Product.objects.count() < 10:
            product_templates = [
                ('Cotton T-Shirt', 'Men Fashion', 499, 999),
                ('Designer Saree', 'Women Fashion', 1299, 2999),
                ('Smart Watch', 'Electronics', 2499, 5999),
                ('Running Shoes', 'Men Fashion', 1599, 3999),
                ('Wireless Earbuds', 'Electronics', 999, 2499),
                ('Denim Jeans', 'Women Fashion', 899, 1999),
                ('Handbag', 'Bags & Footwear', 599, 1499),
                ('Kitchen Set', 'Home & Kitchen', 1999, 4999),
                ('Face Serum', 'Beauty & Health', 399, 799),
                ('Kids Dress', 'Kids', 699, 1299),
            ]

            for name, cat_name, price, original_price in product_templates:
                Product.objects.create(
                    vendor=vendor,
                    category=categories.get(cat_name),
                    brand=random.choice(brands),
                    name=name,
                    slug=slugify(f"{name} {random.randint(1000, 9999)}"),
                    description=f"High quality {name.lower()} available at best price.",
                    price=original_price,
                    discount_price=price,
                    stock=50,
                    is_active=True
                )
            
            self.stdout.write(self.style.SUCCESS('Created dummy products'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
