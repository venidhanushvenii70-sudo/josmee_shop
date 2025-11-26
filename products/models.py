from django.db import models
from vendors.models import Vendor
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome icon class (e.g., fas fa-tshirt)")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class HeroSlider(models.Model):
    title = models.CharField(max_length=200, default="Welcome to Josmee Shopping")
    subtitle = models.CharField(max_length=300, default="Discover Amazing Products from Thousands of Verified Sellers")
    button_text = models.CharField(max_length=50, default="Start Shopping")
    button_link = models.CharField(max_length=200, default="/products/")
    background_image = models.ImageField(upload_to='sliders/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def selling_price(self):
        return self.discount_price if self.discount_price else self.price
    
    @property
    def discount_percentage(self):
        if self.discount_price and self.price > self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'id']
    
    def __str__(self):
        return f"{self.product.name} Image"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About Josmee")
    hero_image = models.ImageField(upload_to='about/', blank=True, null=True)
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_content = models.TextField()
    mission_image = models.ImageField(upload_to='about/', blank=True, null=True)
    values_title = models.CharField(max_length=200, default="Why Choose Us?")
    
    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"
        
    def __str__(self):
        return self.title

class ValueProposition(models.Model):
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='values')
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title

# products/models.py

class Product(models.Model):
    # ... your other fields ...
    is_active = models.BooleanField(default=True)  # <-- Make default True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.vendor.id}")
        super().save(*args, **kwargs)
