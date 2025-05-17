from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Product, Order

def product_list(request):
    products = Product.objects.all()
    ordering = request.GET.get('ordering', '-created_at')  # Default to newest first
    
    # Add ordering
    if ordering:
        products = products.order_by(ordering)
    
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
        products = products.filter(price__lte=float(max_price))

    # Add pagination
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'browse.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)

def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        # Create new order
        order = Order.objects.create(
            product=product,
            customer_name=request.POST.get('name'),
            customer_email=request.POST.get('email'),
            shipping_address=request.POST.get('address'),
            total_price=product.price
        )
        
        # Update product stock
        if product.stock > 0:
            product.stock -= 1
            product.save()
            
            # Redirect to success page with order details
            return render(request, 'checkout_success.html', {
                'product': product,
                'order': order
            })
        else:
            messages.error(request, 'Sorry, this product is out of stock.')
            return redirect('product_detail', product_id=product_id)
    
    context = {
        'product': product,
    }
    return render(request, 'checkout.html', context)

def order_history(request):
    # Get orders for the current user if implemented
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'order_history.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})
