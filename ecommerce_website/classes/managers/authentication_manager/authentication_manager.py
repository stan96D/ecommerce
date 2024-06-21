from ecommerce_website.classes.managers.authentication_manager.base_authentication_manager import *
from ecommerce_website.services.order_info_service.order_info_service import OrderInfoService
from django.contrib.auth import authenticate, login, logout
from ecommerce_website.classes.helpers.shopping_cart_merger import *
from ecommerce_website.services.view_service.order_item_view_service import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import *
from ecommerce_website.classes.managers.mail_manager.mail_manager import *
from django.contrib import messages

class AuthenticationManager(AuthenticationInterface):

    def login(self, request, email, password):
        user = authenticate(request, username=email, password=password)
        if user:

            info_service = OrderInfoService(request)
            shopping_cart_merger = ShoppingCartMerger()
            to_cart = AccountShoppingCart()

            from_cart = SessionShoppingCart(request)

            shopping_cart_merger.merge_from_to(from_cart, to_cart)
            info_service.delete_order()

            login(request, user)
            return True
        else:
            return False

    def sign_up(self, request, form):
        try:
            if not form.is_valid():
                return 'Er is een fout opgetreden bij het registreren van je account.', 'warning'

            user_data = form.save(commit=False)
            password = form.cleaned_data['password1']

            user_data.set_password(password)
            user_data.save()

            if self.login(request, user_data.email, password):
                return 'Account succesvol aangemaakt!', 'success'
            else:
                return 'Er is een fout opgetreden bij het inloggen.', 'warning'

        except Exception as e:
            return 'Er is een onverwachte fout opgetreden.', 'warning'


    def  logout(self, request):
        logout(request)
