from decimal import Decimal, InvalidOperation
from ecommerce_website.classes.helpers.numeric_value_normalizer import extract_value_and_unit
from ecommerce_website.models import ProductAttribute
from ecommerce_website.settings.webshop_config import WebShopConfig


def refactor_product_attributes_to_numeric_values(attribute_names=WebShopConfig.slider_filters()):
    """
    Refactor ProductAttributes by converting their value to a Decimal and storing it in the numeric_value field.

    :param attribute_names: List of ProductAttributeType names to filter by
    """

    attribute_names = ["Dikte toplaag",
                       "Dikte tussenlaag", "Dikte onderlaag", "Slijtlaag"]
    # Fetch all ProductAttributes where the attribute_type.name is in the given list
    product_attributes = ProductAttribute.objects.filter(
        attribute_type__name__in=attribute_names
    )

    # Iterate through each ProductAttribute
    for product_attribute in product_attributes:
        value = product_attribute.value
        print(value)
        try:
            new_value, unit = extract_value_and_unit(value)
            print(new_value, unit)
            if not unit:
                print(
                    "ProductAttribute not created error in unit conversion for additional data UNIT....")
                continue  # Skip this iteration and continue with the next ProductAttribute
            # Convert the value (assumed to be a string) to Decimal
            numeric_value = Decimal(new_value)

            # Update the numeric_value field with the converted Decimal
            product_attribute.numeric_value = numeric_value
            product_attribute.additional_data = {"Unit": unit}
            product_attribute.save()
            print(f"Updated ProductAttribute: {product_attribute}")

        except (ValueError, InvalidOperation) as e:
            # Handle any errors during conversion (e.g., non-numeric values)
            print(f"Failed to convert value '{
                  value}' for ProductAttribute {product_attribute.id}: {e}")
            product_attribute.numeric_value = None  # Set to None if conversion fails
            product_attribute.save()
            print(f"Set numeric_value to None for ProductAttribute {
                  product_attribute.id} due to conversion error.")
