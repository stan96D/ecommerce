from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.product_view import ProductDetailView


class ProductDetailViewService(ViewServiceInterface):

    def generate(self, items):
        productViews = []

        for item in items:
            productView = ProductDetailView(item)
            productViews.append(productView)

        return productViews

    def get(self, item):
        productView = ProductDetailView(item)
        return productView
