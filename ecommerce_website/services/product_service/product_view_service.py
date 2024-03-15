from ecommerce_website.services.product_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.product_view import ProductView

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
