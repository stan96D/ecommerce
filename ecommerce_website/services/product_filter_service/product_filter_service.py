from collections import defaultdict
from decimal import Decimal
from django.db.models import Count
from ecommerce_website.classes.helpers.numeric_value_normalizer import is_value_in_range
from ecommerce_website.models import *
from ecommerce_website.services.product_filter_service.base_product_filter_service import ProductFilterServiceInterface
from django.db.models import Q
from ecommerce_website.classes.model_encapsulator.product_filter_view import *
from ecommerce_website.services.view_service.product_filter_service import *
from ecommerce_website.settings.webshop_config import WebShopConfig
from django.db.models import Min, Max
from decimal import Decimal
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
        return

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
                    matched_filters[search_filter.name] = {
                        "filter_type": search_filter.filter_type,
                        "values": all_attribute_values
                    }

            product_filter_view_service = ProductFilterViewService()
            product_filter_views = product_filter_view_service.generate(
                matched_filters.items())

            return product_filter_views

        except ProductFilter.DoesNotExist:
            return None

    @staticmethod
    def sort_product_filters_on_importance(product_filters, selected_filters=None):
        # Define the order of importance for shopping for floors
        important_filters = [
            "Prijs",
            "Merk",
            "Collectie",
            "Vloertype",
            "Dikte",
            "Toplaagdikte",
            "Lengte",
            "Breedte",
            "Warmteweerstand (m²K/W)"
        ]

        # Initialize the sorting order based on important filters
        filters_order = important_filters.copy()

        if selected_filters:
            for key, value in selected_filters.items():
                # If the selected filter is in important filters, move it to the top of filters_order
                if key in filters_order:
                    filters_order.remove(key)
                # Insert selected filters at the beginning in the order they appear in selected_filters
                filters_order.insert(0, key)

        # Sort the product filters according to the updated filters_order list
        sorted_filters = sorted(
            product_filters,
            key=lambda f: filters_order.index(
                f.name) if f.name in filters_order else len(filters_order)
        )

        # Sort the values alphabetically within each filter
        for filter in sorted_filters:
            if filter.type == "option":
                filter.values = ProductFilterService.sort_product_attributes_alphabetically(
                    filter.values
                )

        return sorted_filters

    @staticmethod
    def sort_product_attributes_alphabetically(product_attributes):
        """Sort the product attributes alphabetically."""
        return sorted(product_attributes, key=str.lower)

    @staticmethod
    def create_filter_for_price(products):
        # Query the lowest and highest effective prices directly from the database
        price_range = products.aggregate(
            min_price=Min('effective_price'),
            max_price=Max('effective_price')
        )

        # Get the lowest and highest prices from the aggregated results
        value_low = price_range['min_price']
        value_high = price_range['max_price']

        # Ensure that the low and high values are properly rounded and converted to Decimal
        values_for_price = [
            Decimal(value_low).quantize(Decimal('0.01')
                                        ) if value_low else Decimal('0.00'),
            Decimal(value_high).quantize(Decimal('0.01')
                                         ) if value_high else Decimal('0.00')
        ]

        # Define the filter item for the price range
        item = {
            "name": "Prijs",
            "values": values_for_price,
            "filter_type": "slider",
            "unit": "€"
        }

        # Assuming the `ProductFilterViewService().get(item)` will process the filter
        product_filter = ProductFilterViewService().get(item)

        return product_filter

    @staticmethod
    def get_product_filters_by_category(category):
        # Fetch all filters for the category
        category_filters = ProductFilter.objects.filter(
            parent_category__name=category)

        # Group filters by their name
        filters_by_name = {}
        for filter in category_filters:
            if filter.name not in filters_by_name:
                filters_by_name[filter.name] = filter
            else:
                # Combine values if filter with the same name already exists
                filters_by_name[filter.name].values = list(
                    set(filters_by_name[filter.name].values + filter.values)
                )

        # Only keep filters with more than one value
        unique_category_filters = [
            filter for filter in filters_by_name.values() if len(filter.values) > 1
        ]

        # Generate views for the unique filters
        product_filter_view_service = ProductFilterViewService()
        product_filter_views = product_filter_view_service.generate(
            unique_category_filters)

        return product_filter_views

    @staticmethod
    def get_product_filters_by_category_sub(category, sub_category):

        category_filters = ProductFilter.objects.filter(Q(parent_category__parent_category__name=category) & Q(parent_category__name=sub_category)
                                                        )
        category_filters = [
            filter for filter in category_filters if len(filter.values) > 1
        ]
        product_filter_view_service = ProductFilterViewService()
        product_filter_views = product_filter_view_service.generate(
            category_filters)

        return product_filter_views

    @staticmethod
    def get_product_filters_by_category_sub_nested(category, sub_category, sub_attribute):

        category_filters = ProductFilter.objects.filter(Q(parent_category__parent_category__parent_category__name=category)
                                                        & Q(parent_category__parent_category__name=sub_category)
                                                        & Q(parent_category__name=sub_attribute))
        category_filters = [
            filter for filter in category_filters if len(filter.values) > 1
        ]
        product_filter_view_service = ProductFilterViewService()
        product_filter_views = product_filter_view_service.generate(
            category_filters)

        return product_filter_views

    @staticmethod
    def get_products_filters_by_products(products, category, current_filters, sub_category=None, sub_attribute=None,):
        start_time = time.time()  # Start the timer

        # Create a dictionary to store attribute values grouped by their type names
        product_attributes = defaultdict(set)  # Using set to avoid duplicates
        product_attribute_units = defaultdict(
            set)  # Using set to avoid duplicates

        slider_filters = WebShopConfig.slider_filters()
        step1_time = time.time()  # Timer for slider filters initialization

        # Populate the product_attributes dictionary
        for product in products:
            for attribute in product.attributes.all():
                if attribute.attribute_type.name in slider_filters:
                    product_attributes[attribute.attribute_type.name].add(
                        attribute.numeric_value,
                    )
                    product_attribute_units[attribute.attribute_type.name].add(
                        attribute.additional_data["Unit"],
                    )
                else:
                    product_attributes[attribute.attribute_type.name].add(
                        attribute.value)

        step2_time = time.time()  # Timer for populating product attributes

        # Convert sets to lists for easier processing later
        for type_name in product_attributes:
            product_attributes[type_name] = list(product_attributes[type_name])

        step3_time = time.time()  # Timer for set-to-list conversion

        category_query = Q(parent_category__name=category)

        if sub_category:
            category_query = Q(parent_category__parent_category__name=category) & Q(
                parent_category__name=sub_category)

        if sub_attribute:
            category_query = Q(
                parent_category__parent_category__parent_category__name=category) & Q(parent_category__parent_category__name=sub_category) & Q(parent_category__name=sub_attribute)

        # Now filter ProductFilter based on the category
        category_filters = ProductFilter.objects.filter(
            category_query
        ).distinct()  # Use distinct() to avoid duplicate filters

        # Combine filters with the same name
        unique_filters = []
        for filter in category_filters:
            # Check if a filter with the same name already exists in the list
            existing_filter = next(
                (f for f in unique_filters if f.name == filter.name), None)

            if existing_filter:
                # Combine values if the filter with the same name exists
                existing_filter.values = list(
                    set(existing_filter.values + filter.values)
                )
            else:
                # Add new filter if it doesn't already exist
                unique_filters.append(filter)

        category_filters = unique_filters

        step4_time = time.time()  # Timer for fetching category filters

        valid_filters = []

        # Iterate through category filters to match with product_attributes
        for product_filter in category_filters:
            # Assuming the ProductFilter model has a 'name' attribute
            filter_name = product_filter.name
            # Check if the filter name matches the product attribute types
            if filter_name in product_attributes:
                # Get the values for the current filter type
                available_values = product_attributes[filter_name]

                if product_filter.filter_type == "slider":

                    if product_attribute_units[filter_name]:
                        available_unit = product_attribute_units[filter_name].pop(
                        )

                    values = available_values

                    product_filter.values = values

                    if not product_filter.unit_value and available_unit:
                        product_filter.unit_value = available_unit

                else:
                    # Collect valid values from product_filter that match available_values
                    valid_values = [
                        value for value in product_filter.values if value in available_values]

                    product_filter.values = valid_values

                if product_filter.name not in current_filters:
                    # Only add filters that have more than one value
                    if len(product_filter.values) > 1:
                        valid_filters.append(product_filter)

                else:
                    # Always add values that are already a filter
                    valid_filters.append(product_filter)

        step5_time = time.time()  # Timer for matching and processing filters

        # Generate the final filters using the service
        product_filter_view_service = ProductFilterViewService()
        product_filter_views = product_filter_view_service.generate(
            valid_filters)

        end_time = time.time()  # End the timer

        # Log the timings
        print(f"Total Execution Time: {end_time - start_time:.4f} seconds")
        print(f"Slider Filters Initialization: {
            step1_time - start_time:.4f} seconds")
        print(f"Populating Product Attributes: {
            step2_time - step1_time:.4f} seconds")
        print(f"Set-to-List Conversion: {step3_time - step2_time:.4f} seconds")
        print(f"Fetching Category Filters: {
              step4_time - step3_time:.4f} seconds")
        print(f"Matching and Processing Filters: {
            step5_time - step4_time:.4f} seconds")
        print(f"Generating Filter Views: {end_time - step5_time:.4f} seconds")

        return product_filter_views  # Return as a list of valid ProductFilter instances

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
                        matched_filters_dict[filter_obj.name].values.append(
                            attribute.value)

                        matched_filters_dict[filter_obj.name].append(
                            attribute.value)

                    else:
                        matched_filters_dict[filter_obj.name].values = [
                            attribute.value]
                        matched_filters_dict[filter_obj.name].filter_type = filter_obj.filter_type

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
                        matched_filters_dict[filter_obj.name].values.append(
                            attribute.value)

                        matched_filters_dict[filter_obj.name].append(
                            attribute.value)

                    else:
                        matched_filters_dict[filter_obj.name].values = [
                            attribute.value]
                        matched_filters_dict[filter_obj.name].filter_type = filter_obj.filter_type

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
