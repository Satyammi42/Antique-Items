from django.shortcuts import render
from product.models import Product
from django.db.models import Q

def home_view(request):
    
    return render(request, 'index.html')