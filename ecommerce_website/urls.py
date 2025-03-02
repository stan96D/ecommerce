from django.urls import path
from . import views
from .sitemaps import *
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'products': ProductSitemap,
    'categories': ProductCategorySitemap,
    'subcategories': ProductSubcategorySitemap,
}

handler404 = 'ecommerce_website.views.custom_404_view'


urlpatterns = [
    # API
    path('get-address/',
         views.get_address, name='get_address'),


    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # Webhooks
    path('mollie_webhook/', views.mollie_webhook, name="mollie_webhook"),
    path('return_payment_webhook/',
         views.return_payment_webhook, name="return_payment_webhook"),

    # Home
    path('', views.home, name="home"),

    # Ratings
    path('store_rating/', views.store_rating_view, name="store_rating"),
    path('create_store_rating/', views.create_store_rating,
         name="create_store_rating"),

    # Account
    path('account/', views.account_view, name="account"),
    path('change_account_information/', views.change_account_information,
         name="change_account_information"),
    path('change_delivery_address_information/', views.change_delivery_address_information,
         name="change_delivery_address_information"),
    path('delete_account/', views.delete_account, name='delete_account'),

    # Authorization
    path('sign_in/', views.sign_in, name="sign_in"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('registration/', views.registration_view, name="registration"),
    path('logout/', views.logout_user, name="logout"),
    path('login/', views.login_view, name="login"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('new_password/<token>/', views.new_password, name='new_password'),

    # Favorites
    path('get-favorite-count/', views.get_favorite_count,
         name='get_favorite_count'),


    # Returns
    path('return_detail/', views.return_detail, name="return_detail"),
    path('return_create/', views.create_return, name="create_return"),
    path('confirm_return/', views.confirm_return, name="confirm_return"),
    path('create_return_overview/',
         views.create_return_overview, name="create_return_overview"),

    path('validate-return-order/',
         views.validate_return_order, name="validate_return_order"),


    # Order
    path('confirm_order/', views.confirm_order, name="confirm_order"),
    path('order_detail/', views.order_detail,
         name="order_detail"),
    path('repay_order/<int:order_id>/', views.repay_order, name='repay_order'),
    path('order_info/', views.order_info, name="order_info"),
    path('order-returnable/', views.order_returnable, name="order_returnable"),

    # Products
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
    path('runners/', views.runner_products, name='runner_products'),
    path('discounts/', views.discount_products, name='discount_products'),

    # Cart
    path('cart/', views.cart, name="cart"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('change-quantity-in-cart/', views.change_quantity_in_cart,
         name='change_quantity_in_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('get-shopping-cart/', views.get_shopping_cart, name='get_shopping_cart'),
    path('delete-cart-item/',
         views.delete_cart_item, name='delete_cart_item'),
    path('checkout/', views.checkout, name="checkout"),
    path('navigate_checkout/', views.navigate_checkout, name="navigate_checkout"),

    # Static views
    path('contact-service/', views.contact_service, name='contact_service'),
    path('payment-return-service/', views.payment_return_service,
         name='payment_return_service'),
    path('return-service/', views.return_service,
         name='return_service'),
    path('about-us/', views.about_us,
         name='about_us'),
    path('terms-and-conditions/', views.static_html_view,
         name='terms_and_conditions'),
    path('disclaimer/', views.static_html_view,
         name='disclaimer')
]
