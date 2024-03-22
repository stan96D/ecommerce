from ecommerce_website.models import Product, ProductAttribute
from ecommerce_website.services.product_service.base_product_service import ProductServiceInterface
from django.db.models import Q

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
    def get_products_by_attributes_and_values(attributes):
        try:

            filters = {}

            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key] = values
                else:
                    filters[key] = [value]  

            query = Q()

            for attr_name, attr_values in filters.items():
                attr_filter = Q(attribute_type__name__iexact=attr_name, value__in=attr_values)
                query |= attr_filter


            product_attributes = ProductAttribute.objects.filter(query).distinct()

            products = [product_attribute.product for product_attribute in product_attributes]

            return products
        except ProductAttribute.DoesNotExist:
            return None

    @staticmethod
    def get_all_products_by_id(product_ids):
        try:
            return Product.objects.filter(id__in=product_ids)
        except Product.DoesNotExist:
            return None
        
