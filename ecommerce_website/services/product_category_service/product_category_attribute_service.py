from ecommerce_website.models import ProductCategoryAttribute
from ecommerce_website.services.product_category_service.base_product_category_attribute_service import ProductCategoryAttributeServiceInterface


class ProductCategoryAttributeService(ProductCategoryAttributeServiceInterface):
    @staticmethod
    def get_product_category_attribute_by_id(product_category_id):
        try:
            return ProductCategoryAttribute.objects.get(id=product_category_id)
        except ProductCategoryAttribute.DoesNotExist:
            return None

    @staticmethod
    def get_all_product_category_attributes():
        try:
            return ProductCategoryAttribute.objects.all()
        except ProductCategoryAttribute.DoesNotExist:
            return None

    @staticmethod
    def get_all_active_product_category_attributes():
        try:
            return ProductCategoryAttribute.objects.filter(active=True)
        except ProductCategoryAttribute.DoesNotExist:
            return None
