from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
#     path('products/', views.products, name='products'),
    path('products/<int:category_id>/', views.products, name='products'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('change-quantity-in-cart/', views.change_quantity_in_cart,
         name='change_quantity_in_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('delete-cart-item/',
         views.delete_cart_item, name='delete_cart_item'),

]
