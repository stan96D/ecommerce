from ecommerce_website.services.product_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.cart_item_view import CartItemView
from ecommerce_website.services.product_service.product_service import ProductService

class CartItemViewService(ViewServiceInterface):

    def generate(self, items):
        cartItemViews = []

        for item in items:
            product_id = item['product_id']
            stock = item['quantity']
            product = ProductService.get_product_by_id(product_id)

            cartItemView = CartItemView(product, stock)
            cartItemViews.append(cartItemView)

        return cartItemViews

    def get(self, item):
        product_id = item['product_id']
        stock = item['quantity']
        product = ProductService.get_product_by_id(product_id)

        cartItemView = CartItemView(product, stock)
        return cartItemView

