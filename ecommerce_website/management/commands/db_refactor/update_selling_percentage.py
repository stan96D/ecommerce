from decimal import Decimal

from ecommerce_website.models import Product


def update_selling_percentage(selling_percentage=Decimal('1.30')):
    """
    Updates the selling_percentage attribute for all products in the Product model.

    :param new_vat: The new selling_percentage value to set for all products. Defaults to Decimal('0.70').
    """
    # Update the VAT for all products
    Product.objects.update(selling_percentage=selling_percentage)

    return
