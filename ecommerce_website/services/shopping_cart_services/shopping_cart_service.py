from ecommerce_website.classes.shopping_cart import ShoppingCart
from ecommerce_website.services.shopping_cart_services.base_shopping_cart_service import AbstractShoppingCartService


class ShoppingCartService(AbstractShoppingCartService):
    def __init__(self, request):
        self.shopping_cart = ShoppingCart(request)

    def add_item(self, product_id, quantity):
        self.shopping_cart.add_item(product_id, quantity)

    def remove_item(self, product_id):
        self.shopping_cart.remove_item(product_id)

    def update_quantity(self, product_id, quantity):
        self.shopping_cart.update_quantity(product_id, quantity)

    def clear_cart(self):
        self.shopping_cart.clear_cart()

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
    def count(self):
        return len(self.shopping_cart.cart_items)
    
    @property
    def count(self):
        return len(self.shopping_cart.cart_items)
