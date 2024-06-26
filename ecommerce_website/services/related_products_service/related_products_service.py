from ecommerce_website.services.related_products_service.base_related_products_service import RelatedProductInterface
from ecommerce_website.models import *

class RelatedProductService(RelatedProductInterface):

    @staticmethod
    def get_related_by_product(product_id):
        try:
            return RelatedProduct.objects.filter(main_product__id=product_id)
        except RelatedProduct.DoesNotExist:
            return None
