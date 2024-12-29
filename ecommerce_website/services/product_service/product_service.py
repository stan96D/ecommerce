from django.forms import FloatField
from ecommerce_website.classes.helpers.product_sorter import QueryProductSorter
from ecommerce_website.classes.helpers.query_builder import QueryBuilder, QueryPrefetcher
from ecommerce_website.models import Product, ProductAttribute, ProductSale
from ecommerce_website.services.product_service.base_product_service import ProductServiceInterface
from django.db.models import Q
from collections import defaultdict
import re
from django.db.models import Prefetch
from decimal import Decimal
from django.db.models import IntegerField
from django.db.models.functions import Cast
from ecommerce_website.settings.webshop_config import WebShopConfig
from django.db.models import F, ExpressionWrapper, DecimalField, Case, When, Q
from django.db.models import F, Case, When, Value, Subquery, OuterRef
from django.db.models import F, Case, When, Value, ExpressionWrapper, DecimalField
from django.db.models.functions import Round


class ProductService(ProductServiceInterface):
    @staticmethod
    def get_product_by_id(product_id):
        try:
            return Product.objects.get(id=product_id)
        except Exception:
            return None

    @staticmethod
    def get_all_products():
        try:
            products = Product.objects.all()
            return list(products)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_misc_products():
        try:
            values_to_check = ["Accessoires",
                               "Plinten", "Folie", "Ondervloeren"]

            products = Product.objects.prefetch_related(

                QueryPrefetcher.createAttributePrefetch(
                    # Apply the custom prefetch for the filtered attributes
                    ['Producttype', 'Eenheid', 'Merk'])
            ).filter(
                Q(attributes__value__in=values_to_check) &
                Q(attributes__attribute_type__name="Producttype")
            ).distinct()

            return list(products)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_attribute(attribute):
        try:
            # Filter products based on the attribute value
            products = Product.objects.prefetch_related(

                QueryPrefetcher.createAttributePrefetch(
                    # Apply the custom prefetch for the filtered attributes
                    ['Producttype', 'Eenheid', 'Merk'])
            ).filter(
                # Filter products by name (optional)
                Q(name__icontains=attribute) |
                # Filter products by attribute value
                Q(attributes__value__iexact=attribute)
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_attribute_sub(attribute, subcategory):
        try:
            # Filter products based on the attribute value
            products = Product.objects.prefetch_related(

                QueryPrefetcher.createAttributePrefetch(
                    # Apply the custom prefetch for the filtered attributes
                    ['Producttype', 'Eenheid', 'Merk'])
            ).filter(

                # Filter products by attribute value
                Q(
                    name__icontains=attribute) |
                Q(attributes__value__iexact=attribute)
            ).filter(Q(attributes__attribute_type__name=subcategory)
                     ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_attribute_sub_nested(attribute, subcategory, subattribute):
        try:
            # Filter products based on the attribute value
            products = Product.objects.prefetch_related(

                QueryPrefetcher.createAttributePrefetch(
                    # Apply the custom prefetch for the filtered attributes
                    ['Producttype', 'Eenheid', 'Merk'])
            ).filter(

                # Filter products by attribute value
                Q(
                    name__icontains=attribute) |
                Q(attributes__value__iexact=attribute)
            ).filter(Q(attributes__attribute_type__name=subcategory)
                     ).filter(Q(attributes__value__iexact=subattribute)).distinct()
            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_assortment():
        try:
            # Filter products based on the attribute value
            products = Product.objects.prefetch_related(

                QueryPrefetcher.createAttributePrefetch(
                    # Apply the custom prefetch for the filtered attributes
                    ['Producttype', 'Eenheid', 'Merk'])
            ).all().distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_runners():
        try:
            # Filter products based on the attribute value
            products = Product.objects.prefetch_related(

                QueryPrefetcher.createAttributePrefetch(
                    # Apply the custom prefetch for the filtered attributes
                    ['Producttype', 'Eenheid', 'Merk'])
            ).filter(
                # Filter products by name (optional)
                Q(runner=True)
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_on_sale():
        try:
            # Filter products based on the attribute value
            products = Product.objects.prefetch_related(

                QueryPrefetcher.createAttributePrefetch(
                    # Apply the custom prefetch for the filtered attributes
                    ['Producttype', 'Eenheid', 'Merk'])
            ).filter(
                # Filter products by name (optional)
                productsale__sale__active=True
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_search(search):
        search_filters = WebShopConfig.search_filters()
        try:
            # Split the search string into individual words
            search_words = search.split()

            # Build the query to ensure all words are in either the product name or specific attributes__value
            search_query = Q()
            for word in search_words:
                # Start with searching in the product name
                search_query &= Q(name__icontains=word)

                # If included_attribute_types is provided, limit the attributes search to those types
                if search_filters:
                    search_query |= Q(
                        attributes__value__icontains=word,
                        attributes__attribute_type__name__in=search_filters
                    )

            # Query the database
            products = Product.objects.prefetch_related(
                'attributes__attribute_type',
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk'])

            ).filter(search_query).distinct()
            return products
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_favorite_cached_products(cache):
        try:
            # Try to get the favorite products from the cache
            # Adjust according to your cache key format
            favorite_product_ids = cache.get('favorites', [])

            if not favorite_product_ids:
                # Return empty queryset if no cached favorites are found
                return Product.objects.none()

            # Filter products based on the cache list of favorite product IDs
            products = Product.objects.prefetch_related(
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk']
                )
            ).filter(
                # Filter products by their IDs if they are in the favorites cache
                id__in=favorite_product_ids,
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_attributes(attributes):
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
                attr_filter = Q(
                    attributes__value__in=attr_values,
                    attributes__attribute_type__name=attr_name
                )
                filtered_products = filtered_products.filter(
                    attr_filter).distinct()

            return filtered_products

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

            return filtered_products
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_sale_products_by_attributes(attributes):
        try:

            filters = defaultdict(set)

            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key].update(values)
                else:
                    filters[key].add(value)

            products = Product.objects.filter(
                productsale__sale__active=True).distinct()

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

            return filtered_products
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_important_products_by_attributes(attributes):
        try:

            filters = defaultdict(set)

            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key].update(values)
                else:
                    filters[key].add(value)

            products = Product.objects.filter(
                Q(runner=True) | Q(productsale__sale__active=True)
            ).distinct()

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

            return filtered_products
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_important_products():
        try:
            important_products = Product.objects.filter(
                Q(runner=True) | Q(productsale__sale__active=True)
            ).distinct()
            return list(important_products)
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
    def get_filtered_products_by_value_and_category(options_filters, slider_filters, category, sub_category=None, subattribute=None):

        category_query = Q()

        if category == "Hardlopers":
            category_query = Q(runner=True)
        elif category == "Kortingen":
            category_query = Q(productsale__sale__active=True)
        elif category != "Assortiment":
            # Start with the base category filter
            category_query = Q(attributes__value__iexact=category) | Q(
                name__icontains=category)

        # Prepare lists to hold queries for option attributes and slider attributes
        option_attribute_queries = []
        slider_attribute_queries = []
        price_threshold = None

        # Create Q objects for options filters
        for key, values in options_filters.items():
            option_attribute_queries.append(
                Q(attributes__attribute_type__name__exact=key,
                  attributes__value__in=values)
            )

        # Separate handling for slider filters and Prijs (price)
        for key, values in slider_filters.items():
            if key == "Prijs":
                # Save threshold value for later execution
                price_threshold = float(values.pop())
            else:
                slider_value = float(values.pop())
                slider_attribute_queries.append(
                    Q(attributes__attribute_type__name__exact=key)
                    & Q(attributes__numeric_value__lt=slider_value)
                )

        # Step 1: Filter products by category and apply options and slider filters
        products_by_category = Product.objects.prefetch_related(
            'attributes__attribute_type',
            QueryPrefetcher.createAttributePrefetch(
                ['Producttype', 'Eenheid', 'Merk'])
        ).filter(category_query).distinct()

        # Check for nested sub_category
        if sub_category:
            products_by_category = products_by_category.filter(Q(attributes__attribute_type__name=sub_category)
                                                               ).distinct()

        # Check for nested sub_category attributes
        if subattribute:
            products_by_category = products_by_category.filter(
                Q(attributes__value__iexact=subattribute))

        # Apply options filters
        for query in option_attribute_queries:
            products_by_category = products_by_category.filter(query)

        # Apply slider filters (excluding Prijs)
        for query in slider_attribute_queries:
            products_by_category = products_by_category.filter(query)

        # Step 2: If the Prijs filter is present, execute it on the filtered products
        if price_threshold is not None:
            shipping_margin = WebShopConfig.shipping_margin()

            products_by_category = products_by_category.annotate(
                # Calculate the modified price (price * (1 - selling_percentage / 100))
                modified_price=ExpressionWrapper(
                    F('price') * F('selling_percentage') * shipping_margin *
                    (1 + F('tax') / 100),  # Dynamic tax rate
                    output_field=DecimalField()
                ),

                # Round the modified price
                rounded_modified_price=Round('modified_price', 2),


                # Check for active sales and calculate the sale price
                # Annotate sale price for active sales
                percentage=Case(
                    When(
                        productsale__sale__active=True,
                        then=ExpressionWrapper(
                            (1.00 - F('productsale__percentage') / 100.00),
                            output_field=DecimalField()
                        )
                    ),
                    default=Value(None),  # No sale, so return None
                    output_field=DecimalField()  # Ensure the type is Decimal
                ),

                # Calculate sale effective price (rounded)
                sale_effective_price=Case(
                    When(
                        productsale__sale__active=True,
                        then=F('rounded_modified_price') * \
                        F('percentage')
                    ),
                    default=Value(None),  # No sale, so return None
                    output_field=DecimalField()
                ),

                # Round the sale effective price
                rounded_sale_effective_price=Round('sale_effective_price', 2),

                # Calculate the final effective price based on the sale status
                effective_price=Case(
                    When(
                        productsale__sale__active=True,
                        then=F('rounded_sale_effective_price')
                    ),
                    # If no sale, use the rounded modified price with shipping
                    default=F('rounded_modified_price'),
                    output_field=DecimalField()
                ),

                # Round the effective price
                rounded_effective_price=Round('effective_price', 2)
            ).filter(
                rounded_effective_price__lt=price_threshold
            )

        return products_by_category

    @staticmethod
    def get_filtered_products_by_search(options_filters, slider_filters, search):
        search_filters = WebShopConfig.search_filters()
        # Split the search string into individual words
        search_words = search.split()

        # Build the query to ensure all words are in either the product name or specific attributes__value
        search_query = Q()
        for word in search_words:
            # Start with searching in the product name
            search_query &= Q(name__icontains=word)

            # If included_attribute_types is provided, limit the attributes search to those types
            if search_filters:
                search_query |= Q(
                    attributes__value__icontains=word,
                    attributes__attribute_type__name__in=search_filters
                )

        # Prepare lists to hold queries for option attributes and slider attributes
        option_attribute_queries = []
        slider_attribute_queries = []
        price_threshold = None

        # Create Q objects for options filters
        for key, values in options_filters.items():
            option_attribute_queries.append(
                Q(attributes__attribute_type__name__exact=key,
                  attributes__value__in=values)
            )

        # Separate handling for slider filters and Prijs (price)
        for key, values in slider_filters.items():
            if key == "Prijs":
                # Save threshold value for later execution
                price_threshold = float(values.pop())
            else:
                slider_value = float(values.pop())
                slider_attribute_queries.append(
                    Q(attributes__attribute_type__name__exact=key)
                    & Q(attributes__numeric_value__lt=slider_value)
                )

        # Step 1: Filter products by category and apply options and slider filters
        products_by_category = Product.objects.prefetch_related(
            'attributes__attribute_type',
            QueryPrefetcher.createAttributePrefetch(
                ['Producttype', 'Eenheid', 'Merk'])
        ).filter(search_query).distinct()

        # Apply options filters
        for query in option_attribute_queries:
            products_by_category = products_by_category.filter(query)

        # Apply slider filters (excluding Prijs)
        for query in slider_attribute_queries:
            products_by_category = products_by_category.filter(query)

        # Step 2: If the Prijs filter is present, execute it on the filtered products
        if price_threshold is not None:
            shipping_margin = WebShopConfig.shipping_margin()

            products_by_category = products_by_category.annotate(
                # Calculate the modified price (price * (1 - selling_percentage / 100))
                modified_price=ExpressionWrapper(
                    F('price') * F('selling_percentage') * shipping_margin *
                    (1 + F('tax') / 100),  # Dynamic tax rate
                    output_field=DecimalField()
                ),

                # Round the modified price
                rounded_modified_price=Round('modified_price', 2),


                # Check for active sales and calculate the sale price
                # Annotate sale price for active sales
                percentage=Case(
                    When(
                        productsale__sale__active=True,
                        then=ExpressionWrapper(
                            (1.00 - F('productsale__percentage') / 100.00),
                            output_field=DecimalField()
                        )
                    ),
                    default=Value(None),  # No sale, so return None
                    output_field=DecimalField()  # Ensure the type is Decimal
                ),

                # Calculate sale effective price (rounded)
                sale_effective_price=Case(
                    When(
                        productsale__sale__active=True,
                        then=F('rounded_modified_price') * \
                        F('percentage')
                    ),
                    default=Value(None),  # No sale, so return None
                    output_field=DecimalField()
                ),

                # Round the sale effective price
                rounded_sale_effective_price=Round('sale_effective_price', 2),

                # Calculate the final effective price based on the sale status
                effective_price=Case(
                    When(
                        productsale__sale__active=True,
                        then=F('rounded_sale_effective_price')
                    ),
                    # If no sale, use the rounded modified price with shipping
                    default=F('rounded_modified_price'),
                    output_field=DecimalField()
                ),

                # Round the effective price
                rounded_effective_price=Round('effective_price', 2)
            ).filter(
                rounded_effective_price__lt=price_threshold
            )

        return products_by_category

    @staticmethod
    def get_filtered_products_by_cache(options_filters, slider_filters, cache):
        # Try to get the favorite products from the cache
        # Adjust according to your cache key format
        favorite_product_ids = cache.get('favorites', [])

        if not favorite_product_ids:
            # Return empty queryset if no cached favorites are found
            return Product.objects.none()

        # Filter products based on the cache list of favorite product IDs
        search_query = Q(id__in=favorite_product_ids)

        # Prepare lists to hold queries for option attributes and slider attributes
        option_attribute_queries = []
        slider_attribute_queries = []
        price_threshold = None

        # Create Q objects for options filters
        for key, values in options_filters.items():
            option_attribute_queries.append(
                Q(attributes__attribute_type__name__exact=key,
                  attributes__value__in=values)
            )

        # Separate handling for slider filters and Prijs (price)
        for key, values in slider_filters.items():
            if key == "Prijs":
                # Save threshold value for later execution
                price_threshold = float(values.pop())
            else:
                slider_value = float(values.pop())
                slider_attribute_queries.append(
                    Q(attributes__attribute_type__name__exact=key)
                    & Q(attributes__numeric_value__lt=slider_value)
                )

        # Step 1: Filter products by category and apply options and slider filters
        products_by_category = Product.objects.prefetch_related(
            'attributes__attribute_type',
            QueryPrefetcher.createAttributePrefetch(
                ['Producttype', 'Eenheid', 'Merk'])
        ).filter(search_query).distinct()

        # Apply options filters
        for query in option_attribute_queries:
            products_by_category = products_by_category.filter(query)

        # Apply slider filters (excluding Prijs)
        for query in slider_attribute_queries:
            products_by_category = products_by_category.filter(query)

        # Step 2: If the Prijs filter is present, execute it on the filtered products
        if price_threshold is not None:
            shipping_margin = WebShopConfig.shipping_margin()

            products_by_category = products_by_category.annotate(
                # Calculate the modified price (price * (1 - selling_percentage / 100))
                modified_price=ExpressionWrapper(
                    F('price') * F('selling_percentage') * shipping_margin *
                    (1 + F('tax') / 100),  # Dynamic tax rate
                    output_field=DecimalField()
                ),

                # Round the modified price
                rounded_modified_price=Round('modified_price', 2),


                # Check for active sales and calculate the sale price
                # Annotate sale price for active sales
                percentage=Case(
                    When(
                        productsale__sale__active=True,
                        then=ExpressionWrapper(
                            (1.00 - F('productsale__percentage') / 100.00),
                            output_field=DecimalField()
                        )
                    ),
                    default=Value(None),  # No sale, so return None
                    output_field=DecimalField()  # Ensure the type is Decimal
                ),

                # Calculate sale effective price (rounded)
                sale_effective_price=Case(
                    When(
                        productsale__sale__active=True,
                        then=F('rounded_modified_price') * \
                        F('percentage')
                    ),
                    default=Value(None),  # No sale, so return None
                    output_field=DecimalField()
                ),

                # Round the sale effective price
                rounded_sale_effective_price=Round('sale_effective_price', 2),

                # Calculate the final effective price based on the sale status
                effective_price=Case(
                    When(
                        productsale__sale__active=True,
                        then=F('rounded_sale_effective_price')
                    ),
                    # If no sale, use the rounded modified price with shipping
                    default=F('rounded_modified_price'),
                    output_field=DecimalField()
                ),

                # Round the effective price
                rounded_effective_price=Round('effective_price', 2)
            ).filter(
                rounded_effective_price__lt=price_threshold
            )

        return products_by_category

    @staticmethod
    def get_products_by_attributes_and_values(attributes, category_data):
        try:
            filters = defaultdict(set)

            # Process the attributes to create filters
            for key, value in attributes.items():
                if ',' in value:
                    values = value.split(',')
                    filters[key].update(values)
                else:
                    filters[key].add(value)

            # Prefetch the specific attributes
            attributes_needed = ['Producttype', 'Eenheid', 'Merk']
            attributes_prefetch = Prefetch(
                'attributes',
                queryset=ProductAttribute.objects.filter(
                    attribute_type__name__in=attributes_needed
                ).only('attribute_type__name', 'value'),
                to_attr='prefetched_attributes'
            )

            # Fetch products with prefetching
            filtered_products = Product.objects.prefetch_related(
                attributes_prefetch)

            # Filter products based on attributes
            for attr_name, attr_values in filters.items():
                attr_filter = Q(
                    **{'prefetched_attributes__attribute_type__name': attr_name}
                )
                filtered_products = filtered_products.filter(
                    attr_filter).distinct()

            # Apply additional category-based filtering
            categories = ProductService().return_nested_categories(category_data)
            index = 1

            for category in categories:
                if index == 2:
                    attr_filter = Q(
                        **{'prefetched_attributes__attribute_type__name': category.name}
                    )
                    filtered_products = filtered_products.filter(
                        attr_filter).distinct()
                else:
                    attr_filter = Q(
                        **{'prefetched_attributes__value__in': [category.name]}
                    )
                    filtered_products = filtered_products.filter(
                        attr_filter).distinct()

                index += 1

            return filtered_products

        except Product.DoesNotExist:
            return None

    @ staticmethod
    def return_nested_categories(category, returned_categories=None):
        if returned_categories is None:
            returned_categories = []

        returned_categories.append(category)

        if category.parent_category:
            ProductService.return_nested_categories(
                category.parent_category, returned_categories)

        return returned_categories[::-1]

    @ staticmethod
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

    @ staticmethod
    def __filter_products_on_search__(products, search_string):

        search_words = search_string.split()

        filtered_products = []
        for product in products:
            product_search_string = product.search_string.lower()
            if all(term.lower() in product_search_string for term in search_words):
                filtered_products.append(product)

        return filtered_products

    @ staticmethod
    def filter_products_on_search(products, search_string):
        search_words = search_string.lower().split()
        regex_pattern = re.compile(
            r'\b(?:' + '|'.join(re.escape(word) for word in search_words) + r')\b')

        filtered_products = [product for product in products if ProductService.matches_search(
            product, regex_pattern)]
        return filtered_products

    @ staticmethod
    def matches_search(product, regex_pattern):
        product_search_string = product.search_string.lower()
        return bool(regex_pattern.search(product_search_string))

    # @ staticmethod
    # def get_products_by_search(search_string):
    #     try:
    #         # Filter and limit the products at the database level
    #         filtered_products = Product.objects.filter(
    #             name__icontains=search_string)[:30]

    #         return filtered_products
    #     except Product.DoesNotExist:
    #         return None

    @ staticmethod
    def get_all_products_by_id(product_ids):
        try:
            products = Product.objects.filter(id__in=product_ids)
            return list(products)
        except Product.DoesNotExist:
            return None

    @ staticmethod
    def get_all_runner_products():
        try:
            products = Product.objects.prefetch_related(

                QueryPrefetcher.createAttributePrefetch(
                    # Apply the custom prefetch for the filtered attributes
                    ['Producttype', 'Eenheid', 'Merk'])
            ).filter(runner=True)
            return list(products)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_related_products(id):
        try:
            product = ProductService.get_product_by_id(id)

            # Get the product's attribute of type "Collectie"
            product_attribute = product.attributes.filter(
                attribute_type__name="Collectie"
            ).values_list('value', flat=True).first()

            if not product_attribute:
                return Product.objects.none()

            # Filter products with the same "Collectie" attribute
            attr_filter = Q(attributes__value=product_attribute,
                            attributes__attribute_type__name="Collectie")
            filtered_products = Product.objects.filter(attr_filter).distinct()

            # Sort, limit results, and load only required fields while keeping the query object
            related_products = filtered_products.order_by(
                'name').only('id', 'name', 'thumbnail')[:6]

            return related_products
        except Product.DoesNotExist:
            return Product.objects.none()
