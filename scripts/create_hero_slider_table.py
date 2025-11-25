import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'josmee_projects.settings')
django.setup()

from products.models import HeroSlider

# Create default hero slider
HeroSlider.objects.get_or_create(
    title="Welcome to Josmee Shopping",
    defaults={
        'subtitle': 'Discover Amazing Products from Thousands of Verified Sellers',
        'button_text': 'Start Shopping',
        'button_link': '/products/',
        'is_active': True,
        'order': 1
    }
)

print("✅ Hero slider table created and default slider added!")
