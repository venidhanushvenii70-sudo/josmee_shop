from django.contrib import admin
from .models import User, Address

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'is_active']
    list_filter = ['user_type', 'is_active']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'city', 'state', 'pincode']
