from django.urls import path
from . import views

urlpatterns = [

    path('mollie_webhook/', views.mollie_webhook, name="mollie_webhook"),
    path('tracking_code_webhook/', views.tracking_code_webhook,
         name="tracking_code_webhook"),

    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('new_password/<token>/', views.new_password, name='new_password'),

    path('logout/', views.logout_user, name="logout"),

    path('store_rating/', views.store_rating_view, name="store_rating"),
    path('create_store_rating/', views.create_store_rating,
         name="create_store_rating"),

    path('account/', views.account_view, name="account"),
    path('change_account_information/', views.change_account_information,
         name="change_account_information"),
    path('change_delivery_address_information/', views.change_delivery_address_information,
         name="change_delivery_address_information"),
    path('delete_account/', views.delete_account, name='delete_account'),

    path('sign_in/', views.sign_in, name="sign_in"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('registration/', views.registration_view, name="registration"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('order_info/', views.order_info, name="order_info"),
    path('navigate_checkout/', views.navigate_checkout, name="navigate_checkout"),

    path('confirm_order/', views.confirm_order, name="confirm_order"),
    path('order_detail/', views.order_detail,
         name="order_detail"),
    path('repay_order/<int:order_id>/', views.repay_order, name='repay_order'),

    path('search/', views.search_products,
         name='search_products'),
    path('products/', views.products,
         name='products'),

    path('favorites/', views.favorite_products,
         name='favorite_products'),
    path('add_to_favorites/', views.add_to_favorites,
         name='add_to_favorites'),
    path('products/<str:category>/', views.products_by_category,
         name='products_by_category'),
    path('products/<str:category>/<str:subcategory>/',
         views.products_by_subcategory, name='products_by_subcategory'),
    path('products/<str:category>/<str:subcategory>/<str:attribute>/',
         views.products_by_attribute, name='products_by_attribute'),
    path('product/<str:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('change-quantity-in-cart/', views.change_quantity_in_cart,
         name='change_quantity_in_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('get-shopping-cart/', views.get_shopping_cart, name='get_shopping_cart'),

    path('delete-cart-item/',
         views.delete_cart_item, name='delete_cart_item'),
    path('runners/', views.runner_products, name='runner_products'),
    path('discounts/', views.discount_products, name='discount_products'),

]
