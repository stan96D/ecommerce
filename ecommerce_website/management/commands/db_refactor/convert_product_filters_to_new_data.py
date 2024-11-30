
from decimal import Decimal
import re
from ecommerce_website.classes.helpers.numeric_value_normalizer import extract_lowest_and_highest
from ecommerce_website.models import ProductAttribute, ProductAttributeType, ProductCategory, ProductFilter
from ecommerce_website.seeders.real_seeder import RealProductFilterSeeder
from ecommerce_website.settings.webshop_config import WebShopConfig
from django.db import transaction


def refactor_product_filters_for_all_products():
    print("refactor for refactor_product_filters_for_all_products started...")

    excluded_attributes = WebShopConfig.excluded_filters()
    attributes_for_slider = WebShopConfig.slider_filters()

    # categories = ProductCategory.objects.all()
    categories = ProductCategory.objects.filter(name="Assortiment")
    product_attribute_types = ProductAttributeType.objects.filter()
    # product_attribute_types = ProductAttributeType.objects.filter(
    #     name__in=["Dikte"])

    # product_attribute_types = ProductAttributeType.objects.filter(
    #     name="Lengte")

    for category in categories:
        print("Now in category: ", category)
        for attribute_type in product_attribute_types:

            is_slider = attribute_type.name in attributes_for_slider

            if not is_slider:

                # No excluded attributes and not the same name as category
                if attribute_type.name != category.name and attribute_type.name not in excluded_attributes:

                    print("Now in attribute_type: ", attribute_type,
                          "for category: ", category)

                    associated_attributes = ProductAttribute.objects.filter(
                        attribute_type=attribute_type)

                    if category.name == "Zoeken" or category.name == "Assortiment":
                        values_for_filter = []
                        unit_value = None

                        for product_attribute in associated_attributes:
                            if attribute_type.id == product_attribute.attribute_type.id:
                                if product_attribute.value not in values_for_filter:
                                    if is_slider:
                                        try:
                                            numeric_value = float(
                                                product_attribute.numeric_value)
                                        except Exception:
                                            numeric_value = None
                                            print("numeric", numeric_value)
                                        if numeric_value is not None:
                                            values_for_filter.append(
                                                numeric_value)
                                        if unit_value is None:
                                            unit_value = product_attribute.additional_data["Unit"]

                                    else:
                                        values_for_filter.append(
                                            product_attribute.value)

                        filter_type = "slider" if is_slider else "option"

                        # Check if the filter already exists
                        product_filter, created = ProductFilter.objects.update_or_create(
                            name=attribute_type.name,
                            parent_category=category,
                            defaults={
                                "values": values_for_filter,
                                "filter_type": filter_type,
                                "unit_value": unit_value,
                            },
                        )

                        if created:
                            print(f"Product filter created: {
                                  product_filter.name}")
                        else:
                            print(f"Product filter updated: {
                                  product_filter.name}")

                    else:
                        product_attributes_with_category = RealProductFilterSeeder.filter_attributes_by_category(
                            category, associated_attributes)

                        if len(product_attributes_with_category) > 0:
                            with transaction.atomic():
                                values_for_filter = []
                                unit_value = None

                                for product_attribute in product_attributes_with_category:
                                    if attribute_type.id == product_attribute.attribute_type.id:
                                        if product_attribute.value not in values_for_filter:
                                            if is_slider:
                                                try:
                                                    numeric_value = float(
                                                        product_attribute.numeric_value)
                                                except Exception:
                                                    numeric_value = None
                                                print("numeric", numeric_value)
                                                if numeric_value is not None:
                                                    values_for_filter.append(
                                                        numeric_value)
                                                if unit_value is None:
                                                    unit_value = product_attribute.additional_data["Unit"]
                                            else:
                                                values_for_filter.append(
                                                    product_attribute.value)

                                filter_type = "slider" if is_slider else "option"

                                # Check if the filter already exists
                                product_filter, created = ProductFilter.objects.update_or_create(
                                    name=attribute_type.name,
                                    parent_category=category,
                                    defaults={
                                        "values": values_for_filter,
                                        "filter_type": filter_type,
                                        "unit_value": unit_value,
                                    },
                                )

                                if created:
                                    print(f"Product filter created: {
                                        product_filter.name}")
                                else:
                                    print(f"Product filter updated: {
                                        product_filter.name}")

    print("RealProductFilterSeeder finished...")
