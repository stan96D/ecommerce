from ecommerce_website.models import ProductFilter
from ecommerce_website.services.product_category_service.base_product_filter_service import ProductFilterServiceInterface


class ProductFilterService(ProductFilterServiceInterface):
    @staticmethod
    def get_product_filter_by_id(product_filter_name):
        try:
            return ProductFilter.objects.get(id=product_filter_name)
        except ProductFilter.DoesNotExist:
            return None

    @staticmethod
    def get_product_filters_by_category_id(product_category_id):
        try:
            return ProductFilter.objects.filter(parent_category_id=product_category_id)
        except ProductFilter.DoesNotExist:
            return None
        
    @staticmethod
    def get_product_filters_by_category_name(product_category_name):
        try:
            return ProductFilter.objects.filter(parent_category__name=product_category_name)
        except ProductFilter.DoesNotExist:
            return None

    @staticmethod
    def get_product_filter_by_name(product_filter_name):
        try:
            return ProductFilter.objects.get(name=product_filter_name)
        except ProductFilter.DoesNotExist:
            return None

    @staticmethod
    def get_all_product_filters():
        try:
            return ProductFilter.objects.all()
        except ProductFilter.DoesNotExist:
            return None




