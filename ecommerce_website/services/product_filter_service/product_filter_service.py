from collections import defaultdict
from django.db.models import Count
from ecommerce_website.models import *
from ecommerce_website.services.product_filter_service.base_product_filter_service import ProductFilterServiceInterface
from django.db.models import Q
from ecommerce_website.classes.model_encapsulator.product_filter_view import *
from ecommerce_website.services.view_service.product_filter_service import *
import time

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
            product_filters = ProductFilter.objects.filter(parent_category__name=product_category_name)

            matched_filters_dict = {}
            for filter_obj in product_filters:

                for attribute in filter_obj.product_attributes.all():
                    
                    if filter_obj.name in matched_filters_dict:
                        matched_filters_dict[filter_obj.name].append(
                        attribute.value)

                    else: 
                        matched_filters_dict[filter_obj.name] = [
                            attribute.value]

            product_filter_view_service = ProductFilterViewService()
            product_filter_views = product_filter_view_service.generate(
                matched_filters_dict.items())
            return product_filter_views
        except ProductFilter.DoesNotExist:
            return None




    @staticmethod
    def get_products_filters_for_search(products):
        try:

            product_attributes = ProductAttribute.objects.filter(
                product__in=products)

            search_filters = ProductFilter.objects.filter(
                parent_category__name="Zoeken")


            product_attributes_by_type = defaultdict(list)
            for attribute in product_attributes:
                if attribute.value not in product_attributes_by_type[attribute.attribute_type]:
                    product_attributes_by_type[attribute.attribute_type].append(
                        attribute.value)

            matched_filters = defaultdict(list)

            for search_filter in search_filters:
                filter_attribute_values = {attr_type: values for attr_type,
                                        values in product_attributes_by_type.items() if attr_type.name == search_filter.name}

                if filter_attribute_values:
                    all_attribute_values = [
                        value for values_list in filter_attribute_values.values() for value in values_list]
                    matched_filters[search_filter.name] = all_attribute_values


            product_filter_view_service = ProductFilterViewService()
            product_filter_views = product_filter_view_service.generate(
                matched_filters.items())


            return product_filter_views

        except ProductFilter.DoesNotExist:
            return None


    @staticmethod
    def get_product_filters_by_product_search(products):
        try:

            product_filters = {}

            for product in products:
                product_attributes = product.attributes.all()

                for product_attribute in product_attributes:

                    attribute_type = product_attribute.attribute_type.name

                    if attribute_type in product_filters:
                        product_filters[attribute_type].product_attributes.add(
                            product_attribute)
                    else:
                        product_filter = ProductFilter.objects.create(
                            name=attribute_type)
                        product_filter.product_attributes.add(product_attribute)
                        product_filters[attribute_type] = product_filter

            return list(product_filters.values())
        except ProductFilter.DoesNotExist:
            return None
        
    @staticmethod
    def get_nested_product_filters_by_category_name(category_name, product_category_name):

        try:
            filters = ProductFilter.objects.filter(
                parent_category__name=product_category_name)
            if category_name:
                filters = filters.filter(
                    parent_category__parent_category__name=category_name)
                print(filters)

            matched_filters_dict = {}
            for filter_obj in filters:

                for attribute in filter_obj.product_attributes.all():

                    if filter_obj.name in matched_filters_dict:
                        matched_filters_dict[filter_obj.name].append(
                            attribute.value)

                    else:
                        matched_filters_dict[filter_obj.name] = [
                            attribute.value]

            product_filter_view_service = ProductFilterViewService()
            product_filter_views = product_filter_view_service.generate(
                matched_filters_dict.items())
            return product_filter_views
        except ProductFilter.DoesNotExist:
            return None
        
    @staticmethod
    def get_double_nested_product_filters_by_category_name(category_name, sub_category_name, product_category_name):
        try:
            filters = ProductFilter.objects.filter(
                parent_category__name=product_category_name)
            if sub_category_name:
                filters = filters.filter(
                    parent_category__parent_category__name=sub_category_name)
            if category_name:
                filters = filters.filter(
                    parent_category__parent_category__parent_category__name=category_name)
                
            matched_filters_dict = {}
            for filter_obj in filters:

                for attribute in filter_obj.product_attributes.all():

                    if filter_obj.name in matched_filters_dict:
                        matched_filters_dict[filter_obj.name].append(
                            attribute.value)

                    else:
                        matched_filters_dict[filter_obj.name] = [
                            attribute.value]

            product_filter_view_service = ProductFilterViewService()
            product_filter_views = product_filter_view_service.generate(
                matched_filters_dict.items())
            return product_filter_views
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




