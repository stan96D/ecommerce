from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.order_item_view import OrderItemView


class OrderItemViewService(ViewServiceInterface):

    def generate(self, items):
        cartItemViews = []
        print(items)
        for item in items:

            cartItemView = OrderItemView(item)
            cartItemViews.append(cartItemView)

        return cartItemViews

    def get(self, item):

        cartItemView = OrderItemView(item)
        return cartItemView
