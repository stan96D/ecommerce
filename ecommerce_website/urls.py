from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('confirm_order/', views.confirm_order, name="confirm_order"),
    path('search/', views.search_products,
         name='search_products'),
    path('products/<str:category>/', views.products_by_category, name='products_by_category'),
    path('products/<str:category>/<str:subcategory>/',
         views.products_by_subcategory, name='products_by_subcategory'),
    path('products/<str:category>/<str:subcategory>/<str:attribute>/',
         views.products_by_attribute, name='products_by_attribute'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('change-quantity-in-cart/', views.change_quantity_in_cart,
         name='change_quantity_in_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('delete-cart-item/',
         views.delete_cart_item, name='delete_cart_item'),

]
