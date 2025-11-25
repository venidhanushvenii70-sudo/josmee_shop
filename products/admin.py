from django.contrib import admin
from .models import Category, Product, ProductImage, Review, HeroSlider, Brand, AboutPage, ValueProposition

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'vendor', 
        'category', 
        'brand', 
        'price', 
        'discount_price',
        'stock', 
        'is_active',
        'created_at'
    ]
    list_filter = ['category', 'is_active', 'vendor', 'created_at']
    search_fields = ['name', 'description', 'vendor__store_name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('vendor', 'name', 'slug', 'description', 'category', 'brand')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']

@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')

class ValuePropositionInline(admin.TabularInline):
    model = ValueProposition
    extra = 1

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    inlines = [ValuePropositionInline]
    
    def has_add_permission(self, request):
        # Only allow one About Page object
        if self.model.objects.exists():
            return False
        return True
