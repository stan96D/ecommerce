from ecommerce_website.models import *
from ecommerce_website.classes.helpers.numeric_value_normalizer import extract_value_and_unit
from ecommerce_website.settings.webshop_config import WebShopConfig


def refactor_product_attributes_for_all_products():  # Renamed function

    attribute_types_for_refactor = WebShopConfig.slider_filters()

    # Fetch all products
    products = Product.objects.all()

    # Iterate over all products and their attributes
    for product in products:
        # Fetch attributes for this product
        attributes = ProductAttribute.objects.filter(product=product)

        for product_attribute in attributes:
            # Assuming name is the field to check
            attribute_type = product_attribute.attribute_type.name
            value = product_attribute.value

            if attribute_type in attribute_types_for_refactor:
                # Extract new value and unit
                new_value, unit = extract_value_and_unit(value)

                # Create or update ProductAttribute instances
                product_attribute, created = ProductAttribute.objects.update_or_create(
                    product=product,
                    attribute_type=product_attribute.attribute_type,
                    defaults={
                        'value': new_value,
                        'additional_data': {"Unit": unit}
                    }
                )
                if created:
                    print(f"Created ProductAttribute for {
                          product.name}: {product_attribute}")
                else:
                    print(f"Updated ProductAttribute for {
                          product.name}: {product_attribute}")
