from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from ..models import Product, ProductCategory


def product_list_view(request):
    """
    Display all products with optional category filtering
    """
    # Get category filter from query parameters
    category_slug = request.GET.get('category', '')
    
    # Base queryset
    products = Product.objects.select_related('category')
    
    # Apply category filter if specified
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Get all categories for filter buttons
    categories = ProductCategory.objects.all().order_by('order')
    
    # Order products
    products = products.order_by('order')
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
    }
    
    return render(request, 'website/product_list.html', context)


def product_detail_view(request, slug):
    """
    Display individual product with related products
    """
    # Get the product or 404
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug
    )
    
    # Get related products (same category, excluding current product)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        pk=product.pk
    ).select_related('category').order_by('order')[:3]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'website/product_detail.html', context)