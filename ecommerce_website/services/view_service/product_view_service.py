from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.product_view import ProductView
import time


class ProductViewService(ViewServiceInterface):

    def generate(self, items):
        productViews = []
        for item in items:
            productView = ProductView(item)
            productViews.append(productView)

        return productViews

    def get(self, item):
        productView = ProductView(item)
        return productView
