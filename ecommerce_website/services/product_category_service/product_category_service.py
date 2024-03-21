from ecommerce_website.models import ProductCategory
from ecommerce_website.services.product_category_service.base_product_category_service import ProductCategoryServiceInterface


class ProductCategoryService(ProductCategoryServiceInterface):
    @staticmethod
    def get_product_category_by_id(product_category_id):
        try:
            return ProductCategory.objects.get(id=product_category_id)
        except ProductCategory.DoesNotExist:
            return None

    @staticmethod
    def get_all_product_categories():
        try:
            return ProductCategory.objects.all()
        except ProductCategory.DoesNotExist:
            return None
        
    @staticmethod
    def get_all_active_product_categories():
        try:
            return ProductCategory.objects.filter(active=True)
        except ProductCategory.DoesNotExist:
            return None
        
    @staticmethod
    def get_all_active_head_product_categories():
        try:
            return ProductCategory.objects.filter(active=True, parent_category=None)
        except ProductCategory.DoesNotExist:
            return None
        



