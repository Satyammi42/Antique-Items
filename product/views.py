from django.shortcuts import render
from django.db.models import Q
from .models import Product

def product_list(request):
    products = Product.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category_filter:
        products = products.filter(category__id=category_filter)

    if min_price:
        products = products.filter(price__gte=float(min_price))

    if max_price:
        products = products.filter(price__lte(float(max_price)))

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'browse.html', context)

