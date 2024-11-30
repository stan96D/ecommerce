from django.db.models import F, Value
from django.db.models.functions import Concat
from enum import Enum
from django.db.models import F, Case, When, Value, ExpressionWrapper, DecimalField
from django.db.models.functions import Round
from django.db.models import Case, When, Value, F, DecimalField
from django.utils.timezone import now
from ecommerce_website.models import ProductAttribute
from ecommerce_website.settings.webshop_config import WebShopConfig
from django.db.models import F, Case, When, Value
from django.db.models import Prefetch


class QueryPrefetcher:
    @staticmethod
    def createAttributePrefetch(specific_attribute_types):
        # Create a custom Prefetch queryset for the attributes you're interested in
        return Prefetch(
            'attributes',  # Prefetch the 'attributes' related field
            queryset=ProductAttribute.objects.filter(
                attribute_type__name__in=specific_attribute_types  # Filter attributes by type name
            ),
            to_attr='filtered_attributes'  # Store the filtered attributes in a custom attribute
        )

class QueryBuilder:

    @staticmethod
    def buildEffectivePrice(query):
        shipping_price = WebShopConfig.shipping_margin()
        return query.annotate(
            modified_price=ExpressionWrapper(
                F('price') * (1 - F('selling_percentage') / 100),
                output_field=DecimalField()
            ),

            # Round the modified price
            rounded_modified_price=Round('modified_price', 2),

            # Calculate the modified price with shipping (round it too)
            modified_price_with_shipping=ExpressionWrapper(
                F('rounded_modified_price') * shipping_price,
                output_field=DecimalField()
            ),

            # Round the modified price with shipping
            rounded_modified_price_with_shipping=Round(
                'modified_price_with_shipping', 2),

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
                    then=F('rounded_modified_price_with_shipping') * \
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
                default=F('rounded_modified_price_with_shipping'),
                output_field=DecimalField()
            ),

            # Round the effective price
            rounded_effective_price=Round('effective_price', 2)
        )
