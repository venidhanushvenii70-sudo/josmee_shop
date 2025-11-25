from django.contrib import admin
from .models import Vendor, Order, Return, Payment, Advertisement, SupportTicket, SellerNotification

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'store_name', 
        'user', 
        'business_name', 
        'contact_number',
        'is_verified', 
        'documents_verified',
        'created_at'
    ]
    list_filter = ['is_verified', 'documents_verified', 'business_type', 'created_at']
    search_fields = ['store_name', 'business_name', 'user__username', 'contact_number', 'email']
    readonly_fields = [
        'created_at', 
        'updated_at',
        'pan_card_image',
        'gst_certificate',
        'bank_proof'
    ]
    
    fieldsets = (
        ('Store Information', {
            'fields': ('user', 'store_name', 'store_description', 'is_verified', 'documents_verified')
        }),
        ('Personal Details', {
            'fields': ('full_name', 'contact_number', 'email')
        }),
        ('Business Details', {
            'fields': (
                'business_name',
                'business_type',
                'business_address',
                'city',
                'state',
                'pincode'
            )
        }),
        ('Tax Documents', {
            'fields': ('pan_number', 'pan_card_image', 'gst_number', 'gst_certificate')
        }),
        ('Bank Details', {
            'fields': (
                'bank_account_number',
                'bank_account_holder',
                'bank_ifsc_code',
                'bank_name',
                'bank_branch',
                'bank_proof'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_vendors', 'reject_vendors']
    
    def approve_vendors(self, request, queryset):
        updated = queryset.update(is_verified=True, documents_verified=True)
        self.message_user(request, f'{updated} vendor(s) approved successfully.')
    approve_vendors.short_description = 'Approve selected vendors'
    
    def reject_vendors(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} vendor(s) rejected.')
    reject_vendors.short_description = 'Reject selected vendors'

@admin.register(SellerNotification)
class SellerNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message', 'vendor__store_name')

admin.site.register(Order)
admin.site.register(Return)
admin.site.register(Payment)
admin.site.register(Advertisement)
admin.site.register(SupportTicket)
