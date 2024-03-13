from ecommerce_website.models import Product

class ProductService:
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
