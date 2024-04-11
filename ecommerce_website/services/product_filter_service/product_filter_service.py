from ecommerce_website.models import *
from ecommerce_website.services.product_filter_service.base_product_filter_service import ProductFilterServiceInterface
from django.db.models import Q

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
    def get_products_filters_for_search(products):
        try:
            product_attributes = ProductAttribute.objects.filter(
                product__in=products)

            search_filters = ProductFilter.objects.filter(
                parent_category__name="Zoeken")

            matched_filters = []
            used_filter_names = []
            id = 1

            for filter in search_filters:

                for product_attribute in product_attributes:
                    if len(filter.product_attributes.filter(value=product_attribute.value)) == 1:
                        if product_attribute.attribute_type in used_filter_names:

                            existing_filter = matched_filters[product_attribute.attribute_type]
                            used_filter_names.append(
                                product_attribute.attribute_type)
                        else:
                            new_filter = ProductFilter(
                                id=id,
                                name=product_attribute.attribute_type
                                )
                            print(new_filter)

                            new_filter.product_attributes.add(product_attribute)
                            used_filter_names.append(
                                product_attribute.attribute_type)
                            matched_filters.append(new_filter)
                            id += 1


            return matched_filters
        except ProductFilter.DoesNotExist:
            return None

    # Create ProductFilterView

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
        print(category_name
              , product_category_name)
        try:
            filters = ProductFilter.objects.filter(
                parent_category__name=product_category_name)
            if category_name:
                filters = filters.filter(
                    parent_category__parent_category__name=category_name)
                print(filters)
            return filters
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
            return filters
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




