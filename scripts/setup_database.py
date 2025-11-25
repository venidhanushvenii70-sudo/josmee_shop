import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'josmee_projects.settings')
django.setup()

from django.core.management import call_command

print("🔄 Running migrations...")
call_command('makemigrations')
call_command('migrate')

print("\n✅ Database setup complete!")
print("\n📋 Next steps:")
print("1. Run: python manage.py createsuperuser (to create admin account)")
print("2. Add your Twilio phone number to settings.py: TWILIO_FROM_NUMBER")
print("3. Run: python manage.py runserver")
print("4. Access admin panel at: http://localhost:8000/admin/")
print("5. Add hero sliders, categories, and products from admin panel")
