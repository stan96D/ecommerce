from datetime import date
from ecommerce_website.services.product_service.product_service import ProductService
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.view_service.create_return_item__view import CreateReturnItemViewService
from ecommerce_website.services.view_service.product_detail_view_service import ProductDetailViewService, ProductRelatedViewService
from ecommerce_website.services.view_service.product_view_service import ProductViewService
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.view_service.cart_item_view_service import CartItemViewService
from ecommerce_website.services.product_category_service.product_category_service import ProductCategoryService
from ecommerce_website.services.order_info_service.order_info_service import OrderInfoService
from ecommerce_website.services.order_service.order_service import OrderService
from ecommerce_website.services.view_service.cart_view_service import CartViewService
from django.forms.models import model_to_dict
from ecommerce_website.classes.helpers.shopping_cart_merger import *
from ecommerce_website.services.view_service.order_item_view_service import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import *
from ecommerce_website.classes.managers.mail_manager.mail_manager import *
from ecommerce_website.services.store_motivation_service.store_motivation_service import StoreMotivationService
from ecommerce_website.services.view_service.store_motivation_view_service import StoreMotivationViewService
from ecommerce_website.services.delivery_method_service.delivery_method_service import *
from ecommerce_website.services.view_service.delivery_method_view_service import *
from ecommerce_website.services.brand_service.brand_service import BrandService
from ecommerce_website.services.return_service.return_service import ReturnService
from ecommerce_website.services.view_service.return_order_view_service import ReturnOrderViewService
from ecommerce_website.services.store_rating_service.store_rating_service import StoreRatingService
from ecommerce_website.services.store_service.store_service import StoreService
from django.core.cache import cache


class ViewServiceUtility:

    @staticmethod
    def get_current_store_data():
        # Check if the store data is cached
        store_data = cache.get('store_data')
        if not store_data:
            # If not found in cache, fetch the active store and convert it to a dictionary
            store = StoreService.get_active_store()

            if store:
                # Convert the store model instance to a dictionary
                store_data = model_to_dict(store)
                # Cache the store data for 1 hour (3600 seconds)
                cache.set('store_data', store_data, timeout=3600)
            else:
                store_data = None  # Return None if no active store is found

        return store_data

    @staticmethod
    def get_store_rating_data():

        mean = StoreRatingService.get_mean()

        return {
            "percentage": mean * 20,
            "mean": mean,
            "range": [0, 1, 2, 3, 4, 5],
            "count": StoreRatingService.get_count(),
            "stars": StoreRatingService.get_star_count(),
            "last": StoreRatingService.get_last(min_rating=4)
        }

    @staticmethod
    def get_header_data():
        header_data = cache.get('header_data')
        if not header_data:
            header_data = ProductCategoryService().get_all_active_head_product_categories()
            cache.set('header_data', header_data, timeout=3600)
        return header_data

    @staticmethod
    def get_current_sale_data():
        current_sale_data = cache.get('current_sale_data')
        if not current_sale_data:
            # Filter active sales where the current date is within the range
            current_date = date.today()
            current_sale_data = Sale.objects.filter(
                active=True,
                begin_date__lte=current_date,
                end_date__gte=current_date
            ).first()

            if current_sale_data:
                cache.set('current_sale_data', current_sale_data, timeout=3600)
        return current_sale_data

    @staticmethod
    def get_payment_methods():
        client = MollieClient()
        payment_methods = client.get_payment_methods()
        return payment_methods

    @staticmethod
    def get_store_motivations():
        # Check if the store motivations data is cached
        store_motivations = cache.get('store_motivations')

        if not store_motivations:
            # If not in cache, fetch the data
            store_motivations_data = StoreMotivationService.get_all_active_motivations()
            # Generate the store motivations view data
            store_motivations = StoreMotivationViewService().generate(store_motivations_data)
            # Cache the result for 1 hour (3600 seconds)
            cache.set('store_motivations', store_motivations, timeout=3600)

        return store_motivations

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

        product = ProductService().get_product_by_id(id)

        if not product:
            return

        return ProductDetailViewService().get(product)

    @staticmethod
    def get_order_info(request):
        return OrderInfoService(request).get_order()

    @staticmethod
    def get_order_by_id(id):
        order = OrderService().get_order_by_id(id)
        return OrderItemViewService().get(order)

    @staticmethod
    def get_order_by_id_authenticated(id, authenticated_user):
        order = OrderService().get_order_by_token(id)

        if not order:
            return None

        if authenticated_user.email != order.email:
            return None

        return OrderItemViewService().get(order)

    @staticmethod
    def get_order_by_id_not_authenticated(id):
        order = OrderService().get_order_by_token(id, True)

        if not order:
            return None

        return OrderItemViewService().get(order)

    @staticmethod
    def get_order_by_id_for_return(id):
        order = OrderService().get_order_with_returnable_lines(id)
        return CreateReturnItemViewService().get(order)

    @staticmethod
    def get_return_order_by_id(id):
        return_order = ReturnService.get_return_by_token(id, True)

        if not return_order:
            return None

        return ReturnOrderViewService().get(return_order)

    @staticmethod
    def get_return_order_by_id_authenticated(id, authenticated_user):
        return_order = ReturnService.get_return_by_token(id)

        if not return_order:
            return None

        if return_order.email_address != authenticated_user.email:
            return None

        return ReturnOrderViewService().get(return_order)

    @staticmethod
    def get_product_views(products):
        return ProductViewService().generate(products)

    @staticmethod
    def get_active_delivery_methods():
        delivery_methods = DeliveryMethodService.get_all_active_delivery_methods()
        return DeliveryMethodViewService().generate(delivery_methods)

    @staticmethod
    def get_active_delivery_methods():
        delivery_methods = DeliveryMethodService.get_all_active_delivery_methods()
        return DeliveryMethodViewService().generate(delivery_methods)

    @staticmethod
    def get_active_takeaway_methods():
        delivery_methods = DeliveryMethodService.get_all_active_takeaway_methods()
        return DeliveryMethodViewService().generate(delivery_methods)

    @staticmethod
    def get_alternative_products(id):
        products = ProductService.get_related_products(id)
        return ProductRelatedViewService().generate(products)

    @staticmethod
    def get_all_brands():
        brands = cache.get('all_brands')  # Check if the brands data is cached
        if not brands:
            # If not found in cache, fetch the brands data
            brands = BrandService.get_all_brands()
            # Cache the brands data for 1 hour (3600 seconds)
            cache.set('all_brands', brands, timeout=3600)
        return brands

    @staticmethod
    def get_misc_products():
        misc_products = ProductService.get_misc_products()
        return ProductViewService().generate(misc_products)
