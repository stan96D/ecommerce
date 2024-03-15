from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('products/', views.products, name='products'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
]
