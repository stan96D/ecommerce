from ecommerce_website.classes.managers.authentication_manager.base_authentication_manager import *
from ecommerce_website.services.order_info_service.order_info_service import OrderInfoService
from django.contrib.auth import authenticate, login, logout
from ecommerce_website.classes.helpers.shopping_cart_merger import *
from ecommerce_website.services.view_service.order_item_view_service import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import *
from ecommerce_website.classes.managers.mail_manager.mail_manager import *

class AuthenticationManager(AuthenticationInterface):

    def login(self, request, email, password):
        user = authenticate(request, username=email, password=password)

        if user:

            info_service = OrderInfoService(request)
            shopping_cart_merger = ShoppingCartMerger()
            to_cart = AccountShoppingCart()

            from_cart = SessionShoppingCart(request)

            shopping_cart_merger.merge_from_to(from_cart, to_cart)
            info_service.delete_order(request)

            login(request, user)
            return True
        else:
            return False

    def  logout(self, request):
        logout(request)
