from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.return_order_view import ReturnOrderView


class ReturnOrderViewService(ViewServiceInterface):

    def generate(self, items):
        productViews = []
        for item in items:
            productView = ReturnOrderView(item)
            productViews.append(productView)

        return productViews

    def get(self, item):
        productView = ReturnOrderView(item)
        return productView
