from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.return_order_create_view import ReturnOrderCreateView


class CreateReturnItemViewService(ViewServiceInterface):

    def generate(self, items):
        cartItemViews = []

        for item in items:

            cartItemView = ReturnOrderCreateView(item)
            cartItemViews.append(cartItemView)

        return cartItemViews

    def get(self, item):

        cartItemView = ReturnOrderCreateView(item)
        return cartItemView
