from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('browse/', views.product_list, name='browse_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]