from ecommerce_website.services.product_service.base_product_stock_service import ProductStockServiceInterface
from ecommerce_website.models import ProductStock


class ProductViewService(ProductStockServiceInterface):
    
    @staticmethod
    def get_stock_by_product_id(product_id):
        try:
            return ProductStock.objects.get(id=product_id)
        except ProductStock.DoesNotExist:
            return None
        
    @staticmethod
    def get_all_stocks_by_id(product_ids):
        try:
            return ProductStock.objects.filter(id__in=product_ids)
        except ProductStock.DoesNotExist:
            return None