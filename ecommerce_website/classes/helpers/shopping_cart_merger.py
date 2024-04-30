from ecommerce_website.classes.model.shopping_cart import *

class ShoppingCartMerger():

    def merge_from_to(self, from_cart: ShoppingCartInterface, to_cart: ShoppingCartInterface):

        for product_id, item in from_cart.cart.items():
            to_cart.add_item(product_id, item['quantity'])

        from_cart.clear_cart()
