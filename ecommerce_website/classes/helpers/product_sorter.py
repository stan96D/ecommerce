from enum import Enum
from django.db.models import F, Case, When, Value, ExpressionWrapper, DecimalField
from django.db.models.functions import Round
from django.db.models.functions import Coalesce
from django.db.models import Subquery, OuterRef, Case, When, Value, F, DecimalField
from django.utils.timezone import now
from django.db.models import F, Case, When, Value, Subquery, OuterRef
from collections import defaultdict
from ecommerce_website.classes.helpers.query_builder import QueryBuilder
from ecommerce_website.models import ProductSale
from ecommerce_website.settings.webshop_config import WebShopConfig
from django.db.models import F, Case, When, Value


class ProductSorter:
    SORT_OPTIONS = {
        'Prijs oplopend': {'attribute': 'price', 'order': 'ascending'},
        'Prijs aflopend': {'attribute': 'price', 'order': 'descending'},
    }

    @classmethod
    def sort_products_by(cls, queryset, sort_option: str) -> list:
        sort_data = cls.SORT_OPTIONS.get(sort_option)
        if sort_data:
            # Determine the sorting attribute (price or sale_price)
            attribute = sort_data['attribute']
            order = sort_data['order']

            # Sort products based on sale price if available, otherwise use regular price
            sorted_queryset = sorted(
                queryset,
                key=lambda x: cls._get_effective_price(
                    x)  # Use sale_price if available
            )

            # Reverse the order if sorting is descending
            if order == 'descending':
                sorted_queryset.reverse()

            return sorted_queryset
        else:
            return queryset

    @staticmethod
    def _get_effective_price(product):
        """Helper method to return the effective price (sale_price if available, else regular price)."""
        return product.sale_price if product.sale_price is not None else product.price

    @staticmethod
    def sort_default(products):
        """Sort products by runner status, sale status, and then by price (effective or regular)."""
        # Precompute effective prices for all products to avoid repeated computation
        for product in products:
            product.effective_price = product.sale_price if product.sale_price is not None else product.price

        # Sort based on precomputed attributes
        return sorted(
            products,
            key=lambda x: (
                not x.runner,  # Runner products (True first)
                x.sale_price is None,  # Products with a sale come before those without
                # Sort by effective price (lowest to highest)
                x.effective_price
            )
        )


class QUERY_SORT_OPTIONS(Enum):
    PRICE_ASC = 'Prijs oplopend'
    PRICE_DESC = 'Prijs aflopend'
    NAME_ASC = 'Alfabetisch A-Z'
    NAME_DESC = 'Alfabetisch Z-A'


class QueryProductSorter:

    @staticmethod
    def sort_by(query, sort_type):

        if sort_type == QUERY_SORT_OPTIONS.PRICE_ASC.value:
            query = QueryBuilder.buildEffectivePrice(query).order_by(
                'effective_price',
            )
        elif sort_type == QUERY_SORT_OPTIONS.PRICE_DESC.value:
            query = QueryBuilder.buildEffectivePrice(query).order_by(
                '-effective_price',
            )
        elif sort_type == QUERY_SORT_OPTIONS.NAME_ASC.value:
            query = QueryBuilder.buildEffectivePrice(query).order_by(
                'name',
            )
        elif sort_type == QUERY_SORT_OPTIONS.NAME_DESC.value:
            query = QueryBuilder.buildEffectivePrice(query).order_by(
                '-name',
            )
        else:
            query = QueryProductSorter.sort_default(query)

        return query


    @staticmethod
    def sort_default(query):

        # Check if the sale effective price is already annotated or not before proceeding
        if 'effective_price' not in query.query.annotations:
            query = QueryBuilder.buildEffectivePrice(query)

        # Continue with the rest of the annotations
        query = query.annotate(
            # Annotate a flag for whether the product is on sale (1 for not on sale, 0 for sale)
            on_sale=Case(
                When(rounded_sale_effective_price__isnull=False,
                     then=Value(0)),  # On sale
                default=Value(1),  # Not on sale
            ),
            # Runner status for sorting (0 for runner first, 1 for non-runner)
            runner_first=Case(
                When(runner=True, then=Value(0)),  # Runner first
                default=Value(1),  # Non-runner
            )
        ).order_by(
            # First, sort by runner status (runner products first)
            'runner_first',
            # Then, sort by sale status (sale items first)
            'on_sale',
            # Then, by calculated sale price (if sale exists)
            'effective_price',

        )

        return query


class ProductSorterUtility:

    @staticmethod
    def create_filters(attributes):

        options_filters = defaultdict(set)
        slider_filters = defaultdict(set)

        slider_filter_options = WebShopConfig.slider_filters()

        slider_filter_options.append("Prijs")

        # Process the attributes to create filters
        for key, value in attributes.items():
            if key in slider_filter_options:
                # This key is a slider filter
                slider_filters[key].add(value)
            else:
                # This key is an option filter
                if ',' in value:
                    values = value.split(',')
                    options_filters[key].update(values)
                else:
                    options_filters[key].add(value)

        return options_filters, slider_filters

    @staticmethod
    def is_paginated(attributes):
        return 'page' in attributes

    @staticmethod
    def is_sort(attributes):
        return 'tn_sort' in attributes

    @staticmethod
    def is_filter(attributes):
        return 'tn_sort' not in attributes and len(
            attributes) > 0 or 'tn_sort' in attributes and len(
            attributes) > 1

    @staticmethod
    def is_search_filter(attributes):
        return ('tn_sort' not in attributes and 'q' not in attributes and len(attributes) > 0) or ('tn_sort' in attributes and 'q' not in attributes and len(attributes) > 1) or (
            'tn_sort' not in attributes and 'q' in attributes and len(attributes) > 1) or ('tn_sort' in attributes and 'q' in attributes and len(attributes) > 2)
