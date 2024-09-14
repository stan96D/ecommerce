from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.product_filter_view import ProductFilterView


class ProductFilterViewService(ViewServiceInterface):

    def generate(self, items):
        productViews = []
        for key, value in items:
            productView = ProductFilterView(key, value)
            productViews.append(productView)

        return productViews

    def get(self, item):
        key, value = next(iter(item.items()))

        productView = ProductFilterView(key, value)
        return productView
