from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('account/', views.account_view, name="account"),

    path('sign_in/', views.sign_in, name="sign_in"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('registration/', views.registration_view, name="registration"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('confirm_order/', views.confirm_order, name="confirm_order"),
    path('order_confirmation/', views.order_confirmation,
         name="order_confirmation"),
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
    path('runners/', views.runner_products, name='runner_products'),
]
