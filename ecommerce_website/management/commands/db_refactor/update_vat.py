from decimal import Decimal

from ecommerce_website.models import Product


def update_vat(new_vat=Decimal('21.00')):
    """
    Updates the VAT attribute for all products in the Product model.

    :param new_vat: The new VAT value to set for all products. Defaults to Decimal('21.00').
    """
    # Update the VAT for all products
    Product.objects.update(tax=new_vat)

    return
