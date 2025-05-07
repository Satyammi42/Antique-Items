from django.contrib import admin
from .models import Product, Review  # Replace with your actual model names

# Register your models here.
admin.site.register(Product)
admin.site.register(Review)