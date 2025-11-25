from django.db import models
from accounts.models import User

class Vendor(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('individual', 'Individual/Proprietorship'),
        ('partnership', 'Partnership'),
        ('llp', 'LLP'),
        ('private_limited', 'Private Limited'),
        ('public_limited', 'Public Limited'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    
    # Business Details
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, default='individual')
    business_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    
    # Store Details
    store_name = models.CharField(max_length=200)
    store_description = models.TextField()
    store_logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)
    
    # Tax Documents
    gst_number = models.CharField(max_length=15, blank=True)
    pan_number = models.CharField(max_length=10)
    pan_card_image = models.ImageField(upload_to='vendor_documents/', blank=True, null=True)
    gst_certificate = models.ImageField(upload_to='vendor_documents/', blank=True, null=True)
    
    # Bank Details
    bank_account_number = models.CharField(max_length=20)
    bank_account_holder = models.CharField(max_length=200)
    bank_ifsc_code = models.CharField(max_length=11)
    bank_name = models.CharField(max_length=100)
    bank_branch = models.CharField(max_length=100)
    bank_proof = models.ImageField(upload_to='vendor_documents/', blank=True, null=True)
    
    # Verification Status
    is_verified = models.BooleanField(default=False)
    documents_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.store_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('ready_to_ship', 'Ready to Ship'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=15)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_id}"

class Return(models.Model):
    RETURN_TYPE_CHOICES = [
        ('rto', 'Return to Origin'),
        ('customer_return', 'Customer Return'),
    ]
    
    RETURN_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns')
    return_type = models.CharField(max_length=20, choices=RETURN_TYPE_CHOICES)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=RETURN_STATUS, default='pending')
    charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Return for {self.order.order_id}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('submitted', 'Submitted'),
        ('upcoming', 'Upcoming'),
        ('paid', 'Paid'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='upcoming')
    payment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment ₹{self.net_amount} - {self.status}"

class Advertisement(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='advertisements')
    product_name = models.CharField(max_length=255)
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Ad for {self.product_name}"

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('catalog', 'Catalog'),
        ('shipping', 'Shipping'),
        ('payment', 'Payment'),
        ('technical', 'Technical'),
        ('other', 'Other'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='support_tickets')
    ticket_id = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Ticket {self.ticket_id}"

class SellerNotification(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.vendor.store_name}"
