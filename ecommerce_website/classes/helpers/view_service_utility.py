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
from ecommerce_website.services.delivery_method_service.delivery_method_service import *
from ecommerce_website.services.view_service.delivery_method_view_service import *
from ecommerce_website.services.brand_service.brand_service import BrandService
from ecommerce_website.services.return_service.return_service import ReturnService
from ecommerce_website.services.view_service.return_order_view_service import ReturnOrderViewService
from ecommerce_website.services.related_products_service.related_products_service import RelatedProductService
from ecommerce_website.services.view_service.related_products_view_service import RelatedProductViewService


class ViewServiceUtility:
    @staticmethod
    def get_header_data():
        return ProductCategoryService().get_all_active_head_product_categories()

    @staticmethod
    def get_payment_methods():
        client = MollieClient()
        payment_methods = client.get_payment_methods()
        return payment_methods

    @staticmethod
    def get_store_motivations():
        store_motivations_data = StoreMotivationService.get_all_active_motivations()
        print(store_motivations_data)
        return StoreMotivationViewService().generate(store_motivations_data)

    @staticmethod
    def get_active_categories():
        active_categories = ProductCategoryService(
        ).get_all_active_head_product_categories()
        return active_categories

    @staticmethod
    def get_runner_products():
        products = ProductService().get_all_runner_products()
        return ProductViewService().generate(products)

    @staticmethod
    def get_orders_by_user(user):
        orders = OrderService().get_orders_by_account(user)
        return OrderItemViewService().generate(orders)

    @staticmethod
    def get_returnable_orders_by_user(user):
        orders = OrderService().get_orders_by_account(user)
        returnable_orders = []

        for order in orders:
            if order.can_be_returned:
                returnable_orders.append(order)

        return OrderItemViewService().generate(returnable_orders)

    @staticmethod
    def get_return_orders_by_user(user):
        orders = ReturnService.get_all_returns_for_user(user)
        return ReturnOrderViewService().generate(orders)

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
        return OrderInfoService(request).get_order()

    @staticmethod
    def get_order_by_id(id):
        order = OrderService().get_order_by_id(id)
        return OrderItemViewService().get(order)

    @staticmethod
    def get_product_views(products):
        return ProductViewService().generate(products)

    @staticmethod
    def get_active_delivery_methods():
        delivery_methods = DeliveryMethodService.get_all_active_delivery_methods()
        return DeliveryMethodViewService().generate(delivery_methods)

    @staticmethod
    def get_alternative_products(id):
        products = ProductService.get_related_products(id)
        return ProductDetailViewService().generate(products)

    @staticmethod
    def get_all_brands():
        return BrandService.get_all_brands()

    @staticmethod
    def get_related_products(id):
        related_products = RelatedProductService.get_related_by_product(id)
        return RelatedProductViewService().generate(related_products)

    @staticmethod
    def get_misc_products():
        misc_products = ProductService.get_misc_products()
        return ProductViewService().generate(misc_products)
