from ecommerce_website.classes.model.shopping_cart import AccountShoppingCart, SessionShoppingCart, ShoppingCartInterface
from ecommerce_website.services.shopping_cart_service.base_shopping_cart_service import AbstractShoppingCartService


class ShoppingCartService(AbstractShoppingCartService):
    def __init__(self, request):

        self.request = request

    @property
    def shopping_cart(self) -> ShoppingCartInterface:

        user = self.request.user

        if user.is_authenticated:
            return AccountShoppingCart()
        else:
            return SessionShoppingCart(self.request)

    def add_item(self, product_id, quantity):
        self.shopping_cart.add_item(product_id, quantity)

    def remove_item(self, product_id):
        self.shopping_cart.remove_item(product_id)

    def update_quantity(self, product_id, quantity):
        self.shopping_cart.update_quantity(product_id, quantity)

    def clear_cart(self):
        self.shopping_cart.clear_cart()

    def quantity_in_cart(self, product_id):
        return self.shopping_cart.quantity_in_cart(product_id)

    def to_json(self):
        return self.shopping_cart.to_json()

    @property
    def cart_items(self):
        return self.shopping_cart.cart_items

    @property
    def total_price(self):
        return self.shopping_cart.total_price

    @property
    def sub_price(self):
        return self.shopping_cart.sub_total

    @property
    def tax_price_high(self):
        return self.shopping_cart.total_tax(21)

    @property
    def tax_price_low(self):
        return self.shopping_cart.total_tax(9)

    @property
    def shipping_price(self):
        return self.shopping_cart.shipping_price

    @property
    def count(self):
        return len(self.shopping_cart.cart_items)

    @property
    def is_valid(self):
        return len(self.shopping_cart.cart_items) > 0
