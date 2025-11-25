"""
Database migration script to create OTP verification table
Run this script to add OTP functionality to your database
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'josmee_projects.settings')
django.setup()

from django.core.management import call_command

print("Creating OTP verification table...")
print("=" * 50)

# Create migrations for accounts app
call_command('makemigrations', 'accounts')

# Apply migrations
call_command('migrate')

print("=" * 50)
print("✓ OTP table created successfully!")
print("\nYou can now use OTP authentication in your application.")
print("\nRemember to:")
print("1. Add your Twilio phone number to settings.py (TWILIO_FROM_NUMBER)")
print("2. Verify your Twilio credentials are correct")
print("3. Test OTP functionality with a valid phone number")
