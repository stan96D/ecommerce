from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.product_view import ProductView
import time


class ProductViewService(ViewServiceInterface):

    def generate(self, items):
     # Start timing
        start_time = time.time()

        print("Starting 'generate' method for generating product views")

        productViews = []
        for item in items:
            productView = ProductView(item)
            productViews.append(productView)

        # Log time taken to generate product views
        print(
            f"Generated product views - Time elapsed: {time.time() - start_time:.4f} seconds")

        return productViews

    def get(self, item):
        productView = ProductView(item)
        return productView
