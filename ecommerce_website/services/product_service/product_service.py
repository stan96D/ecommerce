from ecommerce_website.classes.helpers.query_builder import QueryPrefetcher
from ecommerce_website.models import Product, ProductAttribute
from ecommerce_website.services.product_service.base_product_service import ProductServiceInterface
from django.db.models import Q
from collections import defaultdict
import re
from django.db.models import Prefetch
from ecommerce_website.settings.webshop_config import WebShopConfig
from django.db.models import F, ExpressionWrapper, DecimalField, Case, When, Q
from django.db.models import F, Case, When, Value
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
    def are_products_valid(product_ids):
        """
        Checks if all products with given IDs are active.
        :param product_ids: A list of product IDs
        :return: True if all are active, False otherwise
        """
        products = Product.objects.filter(id__in=product_ids)
        return products.count() == len(product_ids) and all(p.active for p in products)

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
                Q(attributes__attribute_type__name="Producttype") &
                Q(active=True)
            ).distinct()

            return list(products)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_attribute(attribute):
        try:
            products = Product.objects.prefetch_related(
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk']
                )
            ).filter(
                (
                    Q(name__icontains=attribute) |
                    Q(attributes__value__iexact=attribute)
                ) & Q(active=True)
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_attribute_sub(attribute, subcategory):
        try:
            products = Product.objects.prefetch_related(
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk']
                )
            ).filter(
                Q(name__icontains=attribute) |
                Q(attributes__value__iexact=attribute)
            ).filter(
                Q(attributes__attribute_type__name=subcategory)
            ).filter(
                active=True
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_attribute_sub_nested(attribute, subcategory, subattribute):
        try:
            products = Product.objects.prefetch_related(
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk']
                )
            ).filter(
                (
                    Q(name__icontains=attribute) |
                    Q(attributes__value__iexact=attribute)
                ) & Q(active=True)
            ).filter(
                Q(attributes__attribute_type__name=subcategory)
            ).filter(
                Q(attributes__value__iexact=subattribute)
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_assortment():
        try:
            products = Product.objects.prefetch_related(
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk']
                )
            ).filter(
                active=True
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_runners():
        try:
            products = Product.objects.prefetch_related(
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk']
                )
            ).filter(
                Q(runner=True) & Q(active=True)
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_on_sale():
        try:
            products = Product.objects.prefetch_related(
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk']
                )
            ).filter(
                Q(productsale__sale__active=True) & Q(active=True)
            ).distinct()

            return products

        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_products_by_search(search):
        search_filters = WebShopConfig.search_filters()
        try:
            search_words = search.split()
            search_query = Q()

            for word in search_words:
                search_query &= (Q(name__icontains=word)
                                 | Q(sku__icontains=word))

                if search_filters:
                    search_query |= Q(
                        attributes__value__icontains=word,
                        attributes__attribute_type__name__in=search_filters
                    )

            products = Product.objects.prefetch_related(
                'attributes__attribute_type',
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk'])
            ).filter(search_query & Q(active=True)).distinct()

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
                ['Producttype', 'Eenheid', 'Merk']
            )
        ).filter(
            category_query,
            active=True  # Ensure product is active
        ).distinct()

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
                        then=F('rounded_modified_price') *
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

        # Build the query to ensure all words are in either the product name, sku, or specific attributes__value
        search_query = Q()
        for word in search_words:
            # Search in the product name or sku
            search_query &= (Q(name__icontains=word) | Q(sku__icontains=word))

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

        products_by_category = Product.objects.prefetch_related(
            'attributes__attribute_type',
            QueryPrefetcher.createAttributePrefetch(
                ['Producttype', 'Eenheid', 'Merk']
            )
        ).filter(
            search_query,
            active=True  # Ensure product is active
        ).distinct()

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
                        then=F('rounded_modified_price') *
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
                ['Producttype', 'Eenheid', 'Merk']
            )
        ).filter(
            search_query,
            active=True  # Ensure product is active
        ).distinct()


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
                        then=F('rounded_modified_price') *
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
    def get_all_runner_products():
        try:
            products = Product.objects.prefetch_related(
                QueryPrefetcher.createAttributePrefetch(
                    ['Producttype', 'Eenheid', 'Merk']
                )
            ).filter(
                runner=True,
                active=True  # Ensure product is active
            )
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
            attr_filter = Q(
                attributes__value=product_attribute,
                attributes__attribute_type__name="Collectie",
                active=True
            )
            filtered_products = Product.objects.filter(attr_filter).distinct()

            # Sort, limit results, and load only required fields while keeping the query object
            related_products = filtered_products.order_by(
                'name').only('id', 'name', 'thumbnail_url')[:6]

            return related_products
        except Product.DoesNotExist:
            return Product.objects.none()
