from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.product_category_view import ProductCategoryView



class ProductCategoryViewService(ViewServiceInterface):

    def generate(self, items):
        productCategoryAttributeViews = []

        for item in items:
            productCategoryAttributeView = ProductCategoryView(item)
            productCategoryAttributeViews.append(productCategoryAttributeView)

        return productCategoryAttributeViews

    def get(self, item):
        productCategoryAttributeView = ProductCategoryView(item)
        return productCategoryAttributeView
