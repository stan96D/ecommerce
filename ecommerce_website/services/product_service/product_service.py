from ecommerce_website.models import Product, ProductAttribute
from ecommerce_website.services.product_service.base_product_service import ProductServiceInterface
from django.db.models import Q
from collections import defaultdict
from django.db.models import Exists, OuterRef
import re

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
    def get_products_by_attributes_and_values(attributes, category_data):
        try:    

            filters = defaultdict(set)

            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key].update(values)
                else:
                    filters[key].add(value)

            filtered_products = Product.objects.all()

            for attr_name, attr_values in filters.items():

                attr_filter = Q(attributes__value__in=attr_values,
                                    attributes__attribute_type__name=attr_name)
                filtered_products = filtered_products.filter(attr_filter).distinct()
      

            categories = ProductService().return_nested_categories(category_data)

            index = 1

            for category in categories:

                if index == 2:

                    attr_filter = Q(attributes__attribute_type__name=category.name)
                    filtered_products = filtered_products.filter(
                        attr_filter).distinct()
                else:
                    attr_filter = Q(attributes__value__in=[category.name])
                    filtered_products = filtered_products.filter(
                                attr_filter).distinct()

                index += 1 

            return filtered_products
        except Product.DoesNotExist:
            return None
        

    @staticmethod
    def return_nested_categories(category, returned_categories=None):
        if returned_categories is None:
            returned_categories = []

        returned_categories.append(category)

        if category.parent_category:
            ProductService.return_nested_categories(
                category.parent_category, returned_categories)

        return returned_categories[::-1]
    

    @staticmethod
    def get_products_by_attributes_and_search(attributes, search_string):
        try:
            print("SEARCH_STRING", search_string)
            filters = defaultdict(set)

            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key].update(values)
                else:
                    filters[key].add(value)

            filtered_products = Product.objects.all()
            
            for attr_name, attr_values in filters.items():

                attr_filter = Q(attributes__value__in=attr_values,
                                    attributes__attribute_type__name=attr_name)
                filtered_products = filtered_products.filter(
                        attr_filter).distinct()

            filtered_products = ProductService().__filter_products_on_search__(
                filtered_products, search_string)
            
            return filtered_products
        except Product.DoesNotExist:
            return None

    @staticmethod
    def __filter_products_on_search__(products, search_string):

        search_words = search_string.split()

        filtered_products = []
        for product in products:
            product_search_string = product.search_string.lower()
            if all(term.lower() in product_search_string for term in search_words):
                filtered_products.append(product)

        return filtered_products
    
    @staticmethod
    def filter_products_on_search(products, search_string):
        search_words = search_string.lower().split()
        regex_pattern = re.compile(
            r'\b(?:' + '|'.join(re.escape(word) for word in search_words) + r')\b')

        filtered_products = [product for product in products if ProductService.matches_search(
            product, regex_pattern)]
        return filtered_products

    @staticmethod
    def matches_search(product, regex_pattern):
        product_search_string = product.search_string.lower()
        return bool(regex_pattern.search(product_search_string))

    @staticmethod
    def get_products_by_search(search_string):
        try:

            products = Product.objects.all()

            filtered_products = ProductService().__filter_products_on_search__(
                products, search_string)

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
        
