from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ecommerce_website.services.view_service.order_info_view_service import OrderInfoViewService
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect, render
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.view_service.product_detail_view_service import ProductDetailViewService
from ecommerce_website.services.view_service.product_view_service import ProductViewService
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.view_service.cart_item_view_service import CartItemViewService
from ecommerce_website.services.product_category_service.product_category_service import ProductCategoryService
from ecommerce_website.services.product_filter_service.product_filter_service import ProductFilterService
from ecommerce_website.classes.helpers.product_sorter import ProductSorter
from ecommerce_website.classes.model.address_info import AddressInfo
from ecommerce_website.classes.model.contact_info import ContactInfo
from ecommerce_website.classes.model.payment_info import PaymentInfo
from ecommerce_website.classes.model.delivery_info import DeliveryInfo
from ecommerce_website.services.order_info_service.order_info_service import OrderInfoService
from ecommerce_website.services.checkout_service.checkout_service import CheckoutService
from ecommerce_website.services.order_service.order_service import OrderService
from ecommerce_website.services.view_service.cart_view_service import CartViewService
from django.http import JsonResponse, HttpResponseBadRequest
import json
from ecommerce_website.classes.forms.user_creation_form import CustomUserCreationForm
from ecommerce_website.classes.helpers.shopping_cart_merger import *
from ecommerce_website.services.view_service.order_item_view_service import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import *
from ecommerce_website.classes.managers.mail_manager.mail_manager import *
from ecommerce_website.services.store_motivation_service.store_motivation_service import StoreMotivationService
from ecommerce_website.services.view_service.store_motivation_view_service import StoreMotivationViewService
from ecommerce_website.classes.managers.authentication_manager.authentication_manager import AuthenticationManager


class ViewServiceUtility:
    @staticmethod
    def get_header_data():
        return ProductCategoryService().get_all_active_head_product_categories()

    @staticmethod
    def get_store_motivations():
        store_motivations_data = StoreMotivationService.get_all_active_motivations()
        return StoreMotivationViewService().generate(store_motivations_data)

    @staticmethod
    def get_active_categories():
        active_categories = ProductCategoryService().get_all_active_head_product_categories()
        return active_categories

    @staticmethod
    def get_runner_products():
        products = ProductService().get_all_runner_products()
        return ProductViewService().generate(products)
    
    @staticmethod
    def get_orders_by_user(user):
        orders =  OrderService().get_orders_by_account(user)
        return OrderItemViewService().generate(orders)

    @staticmethod
    def get_cart_items_view(request):
        items = ShoppingCartService(request).cart_items
        return CartItemViewService().generate(items)

    @staticmethod
    def get_cart_view(request):
        return CartViewService().get(ShoppingCartService(request))

    @staticmethod
    def get_product_view_by_id(id):
        return ProductDetailViewService().get(
            ProductService().get_product_by_id(id))

    @staticmethod
    def get_order_info(request):
        return  OrderInfoService(request).get_order()

    @staticmethod
    def get_order_by_id(id):
        return OrderService().get_order_by_id(id)

    @staticmethod
    def get_product_views(products):
        return ProductViewService().generate(products)
