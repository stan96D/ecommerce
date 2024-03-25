from ecommerce_website.models import Product, ProductAttribute
from ecommerce_website.services.product_service.base_product_service import ProductServiceInterface
from django.db.models import Q
from collections import defaultdict

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
            products = Product.objects.all()
            return list(products)
        except Product.DoesNotExist:
            return None
        
    @staticmethod
    def get_products_by_attribute(attribute):
        try:
            products = Product.objects.filter(attributes__value__iexact=attribute)
            return list(products)
        except Product.DoesNotExist:
            return None
        
    @staticmethod
    def get_products_by_attribute_from_category(attribute, category):
        try:
            product_attributes = ProductAttribute.objects.filter(
                value__iexact=attribute)

            unique_product_ids = set()

            unique_products = []
            for product_attribute in product_attributes:
                product_id = product_attribute.product.id
                if product_id not in unique_product_ids:
                    if product_attribute.product.attributes.filter(value__iexact=category).exists():
                        unique_product_ids.add(product_id)
                        unique_products.append(product_attribute.product)

            return unique_products
        except Product.DoesNotExist:
            return None
        

    @staticmethod
    def get_products_by_attributes_and_values(attributes, category):
        try:    
            filters = defaultdict(set)

            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key].update(values)
                else:
                    filters[key].add(value)

            query = Q()

            for attr_name, attr_values in filters.items():
                attr_filter = Q(
                    attribute_type__name__iexact=attr_name, value__in=attr_values)
                query |= attr_filter
                print(query)

            product_attributes = ProductAttribute.objects.filter(query).distinct()

            unique_product_ids = set()

            unique_products = []
            for product_attribute in product_attributes:
                product_id = product_attribute.product.id
                if product_id not in unique_product_ids:
                    if product_attribute.product.attributes.filter(value__iexact=category).exists():
                        unique_product_ids.add(product_id)
                        unique_products.append(product_attribute.product)

        
            return unique_products
        except ProductAttribute.DoesNotExist:
            return None
        

    @staticmethod
    def get_products_by_search(search_string):
        try:
            product_attributes = ProductAttribute.objects.filter(
                value__icontains=search_string)

            unique_product_ids = set()

            for product_attribute in product_attributes:
                unique_product_ids.add(product_attribute.product.id)

            return Product.objects.filter(id__in=unique_product_ids)

        except ProductAttribute.DoesNotExist:
            return None

    @staticmethod
    def get_all_products_by_id(product_ids):
        try:
            products = Product.objects.filter(id__in=product_ids)
            return list(products)
        except Product.DoesNotExist:
            return None
        
