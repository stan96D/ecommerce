from ecommerce_website.models import Product
from ecommerce_website.services.product_service.base_product_service import ProductServiceInterface

class ProductService(ProductServiceInterface):
    @staticmethod
    def get_product_by_id(product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_all_products():
        try:
            return Product.objects.all()
        except Product.DoesNotExist:
            return None
        
    @staticmethod
    def get_products_by_attribute(attribute):
        try:
            products = Product.objects.filter(attributes__value__iexact=attribute)
            return products
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_all_products_by_id(product_ids):
        try:
            return Product.objects.filter(id__in=product_ids)
        except Product.DoesNotExist:
            return None
        
