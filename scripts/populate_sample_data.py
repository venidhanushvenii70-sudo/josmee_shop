"""
Populate sample data for Josmee Online Shopping
Run this after migrations to add test products and categories
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'josmee_projects.settings')
django.setup()

from products.models import Category, Product
from accounts.models import User
from decimal import Decimal

print("Populating sample data...")
print("=" * 50)

# Create categories
categories_data = [
    {'name': 'Fashion', 'slug': 'fashion', 'icon': 'fas fa-tshirt'},
    {'name': 'Electronics', 'slug': 'electronics', 'icon': 'fas fa-mobile-alt'},
    {'name': 'Home & Living', 'slug': 'home-living', 'icon': 'fas fa-home'},
    {'name': 'Jewelry', 'slug': 'jewelry', 'icon': 'fas fa-gem'},
    {'name': 'Beauty', 'slug': 'beauty', 'icon': 'fas fa-spa'},
    {'name': 'Sports', 'slug': 'sports', 'icon': 'fas fa-football-ball'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults=cat_data
    )
    if created:
        print(f"✓ Created category: {category.name}")

print("\n" + "=" * 50)
print("✓ Sample data populated successfully!")
print("\nYou can now:")
print("1. Visit the homepage to see categories")
print("2. Add products through the admin panel")
print("3. Test the shopping experience")
