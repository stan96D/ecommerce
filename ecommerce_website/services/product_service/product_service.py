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
            products = Product.objects.filter(
                Q(attributes__value__iexact=attribute) |
                Q(name__icontains=attribute)
            ).distinct()  
            return list(products)
        except Product.DoesNotExist:
            return None
        
    @staticmethod
    def get_runner_products():
        try:
            products = Product.objects.filter(runner=True)
            return list(products)
        except Product.DoesNotExist:
            return None
        

    @staticmethod
    def get_runner_products_by_attributes(attributes):
        try:

            filters = defaultdict(set)

            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key].update(values)
                else:
                    filters[key].add(value)

            print(filters)

            products = Product.objects.filter(runner=True)

            filtered_products = []
            for product in products:
                matches_any_attribute = False

                for attr_name, attr_values in filters.items():

                    for attr_value in attr_values:
                        if product.attributes.filter(attribute_type__name__iexact=attr_name, value__iexact=attr_value).exists():
                            matches_any_attribute = True
                            break
                    if matches_any_attribute:
                        break
                if matches_any_attribute:
                    filtered_products.append(product)


            print(filtered_products)
            return filtered_products
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

            product_attributes = ProductAttribute.objects.filter(query).distinct()

            unique_product_ids = set()

            unique_products = []
            for product_attribute in product_attributes:
                product_id = product_attribute.product.id
                if product_id not in unique_product_ids:

                    if product_attribute.product.attributes.filter(value__iexact=category).exists():
                        unique_product_ids.add(product_id)
                        unique_products.append(product_attribute.product)

            print(unique_products)
            return unique_products
        except ProductAttribute.DoesNotExist:
            return None
        

    @staticmethod
    def get_products_by_attributes_and_search(attributes, search):
        try:
            filters = defaultdict(set)
            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key].update(values)
                else:
                    filters[key].add(value)

            attribute_query = Q()
            for attr_name, attr_values in filters.items():
                attr_filter = Q(
                    attribute_type__name__iexact=attr_name, value__in=attr_values)
                attribute_query |= attr_filter

            product_attributes = ProductAttribute.objects.filter(
                attribute_query).distinct()

            unique_product_ids = set()

            unique_products = []

            for product_attribute in product_attributes:
                product_id = product_attribute.product.id
                if product_id not in unique_product_ids:

                    product_search_string = product_attribute.product.search_string.lower()
                    search_terms = search.split()
                    if all(term.lower() in product_search_string for term in search_terms):

                        unique_product_ids.add(product_id)
                        unique_products.append(product_attribute.product)

            return unique_products
        except ProductAttribute.DoesNotExist:
            return None


    @staticmethod
    def get_products_by_search(search_string):
        try:

            search_words = search_string.split()

            products = Product.objects.all()

            filtered_products = []
            for product in products:
                product_search_string = product.search_string.lower()
                if all(term.lower() in product_search_string for term in search_words):
                    filtered_products.append(product)

            return filtered_products
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_all_products_by_id(product_ids):
        try:
            products = Product.objects.filter(id__in=product_ids)
            return list(products)
        except Product.DoesNotExist:
            return None
        
    @staticmethod
    def get_all_runner_products():
        try:
            products = Product.objects.filter(runner=True)
            return list(products)
        except Product.DoesNotExist:
            return None
        
