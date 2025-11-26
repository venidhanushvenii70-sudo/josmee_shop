from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Case, When, IntegerField
from django.core.paginator import Paginator
from .models import Product, Category, HeroSlider, Brand, AboutPage

def home(request):
    featured_products = Product.objects.filter(is_active=True).order_by('?')[:12]
    deals_products = Product.objects.filter(is_active=True, discount_price__isnull=False).order_by('?')[:8]
    categories = Category.objects.all()[:10]
    hero_sliders = HeroSlider.objects.filter(is_active=True).order_by('order')
    brands = Brand.objects.filter(is_featured=True)[:12]  # Increased for grid

    return render(request, 'products/home.html', {
        'recommendations': featured_products, 
        'deals_products': deals_products,
        'categories': categories,
        'hero_sliders': hero_sliders,
        'brands': brands,
    })

def deals(request):
    products = Product.objects.filter(is_active=True, discount_price__isnull=False)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'page_title': 'Deals & Offers',
        'is_deals': True
    })

def new_arrivals(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:50]
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'page_title': 'New Arrivals'
    })

def about(request):
    about_content = AboutPage.objects.first()
    return render(request, 'products/about.html', {'about_content': about_content})

def product_list(request):
    products = Product.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if search_query:
        search_query = search_query.strip()
        
        # Search across multiple fields
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).select_related('brand', 'category').prefetch_related('images')
        
        # Add relevance ranking (name matches get higher priority)
        products = products.annotate(
            relevance=Case(
                When(name__iexact=search_query, then=3),
                When(name__istartswith=search_query, then=2),
                When(name__icontains=search_query, then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-relevance', '-created_at')
    else:
        # Optimize query with select_related and prefetch_related
        products = products.select_related('brand', 'category').prefetch_related('images')
    
    # Add pagination for better performance
    paginator = Paginator(products, 24)  # 24 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products_page,  # Changed from products to products_page
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'page_title': 'All Products'
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

# products/views.py

def home(request):
    # Show 12 random active products
    featured_products = Product.objects.filter(is_active=True).order_by('?')[:12]
    
    deals_products = Product.objects.filter(is_active=True, discount_price__isnull=False).order_by('?')[:8]
    
    categories = Category.objects.all()[:10]
    hero_sliders = HeroSlider.objects.filter(is_active=True).order_by('order')
    brands = Brand.objects.filter(is_featured=True)[:12]

    return render(request, 'products/home.html', {
        'recommendations': featured_products,
        'deals_products': deals_products,
        'categories': categories,
        'hero_sliders': hero_sliders,
        'brands': brands,
    })
