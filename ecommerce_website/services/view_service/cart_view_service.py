from ecommerce_website.services.view_service.base_view_service import SingleViewServiceInterface
from ecommerce_website.classes.model_encapsulator.cart_item_view import CartView


class CartViewService(SingleViewServiceInterface):

    def get(self, item):

        cart_view = CartView(item.total_price,
                             item.sub_price,
                             item.tax_price_high,
                             item.tax_price_low,
                             item.shipping_price)

        return cart_view
