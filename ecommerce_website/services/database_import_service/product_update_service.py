from decimal import Decimal
from ecommerce_website.classes.managers.progress_manager.progress_manager import ProgressManager
from ecommerce_website.seeders.initial_seeder_data.category_data import category_data
from ecommerce_website.services.database_import_service.base_database_import_service import DatabaseImportServiceInterface
from ecommerce_website.db_mapper.sql_db_mapper import SQLDatabaseMapper
from ecommerce_website.models import *
from ecommerce_website.db_mapper.data import *
from django.db import transaction
from ecommerce_website.classes.helpers.numeric_value_normalizer import extract_value_and_unit

from ecommerce_website.services.product_filter_service.product_filter_service import ProductFilterService
from ecommerce_website.settings.webshop_config import *

slider_filters = WebShopConfig.slider_filters()


class ProductUpdateService(DatabaseImportServiceInterface):

    def __init__(self, progress_service=None):
        self.progress_service = progress_service or ProgressManager()

    def detect_changes(self, obj, new_data):
        """
        Compare an object's fields with new data and return the differences.
        """
        changes = {}
        for field, new_value in new_data.items():
            old_value = getattr(obj, field, None)

            # Normalize numbers for comparison
            if isinstance(old_value, (Decimal, float, int)) or isinstance(new_value, (Decimal, float, int)):
                try:
                    old_value = float(old_value)
                    new_value = float(new_value)
                except (ValueError, TypeError):
                    pass  # Leave as-is for direct comparison

            if old_value != new_value:
                changes[field] = {"from": str(old_value), "to": str(new_value)}
        return changes

    def import_product_data(self, json_data):
        mapper = SQLDatabaseMapper()
        products, attributes, types = mapper.map_products(json_data)
        self.import_product_attribute_types(types)
        product_report = self.import_products(products)
        attribute_report = self.import_attributes(attributes)
        category_report = self.update_categories(json_data)
        filters_report = self.update_product_filters()
        return {
            "products": product_report,
            "attributes": attribute_report,
            "categories": category_report,
            "filters": filters_report
        }

    def import_product_attribute_types(self, types):
        report = {"created": [], "updated": [], "failed": [], "changes": []}

        # Start the task with total steps equal to the number of types to import
        self.progress_service.start_task(
            "Import Product Attribute Types", total_steps=len(types))

        for type_data in types:
            try:
                product_attribute_type, created = ProductAttributeType.objects.get_or_create(
                    name=type_data["name"]
                )
                if created:
                    print(f"ProductAttributeType '{
                          product_attribute_type.name}' created.")
                    report["created"].append(type_data["name"])
                else:
                    print(f"ProductAttributeType '{
                          product_attribute_type.name}' already exists.")
                    report["updated"].append(type_data["name"])

            except Exception as e:
                print(f"Failed to handle ProductAttributeType '{
                      type_data['name']}': {str(e)}")
                report["failed"].append(
                    {"type": type_data["name"], "error": str(e)}
                )

            # Update progress after processing each attribute type
            self.progress_service.update_task(
                "Import Product Attribute Types", steps=1)

        # Complete the task when all attribute types are processed
        self.progress_service.complete_task("Import Product Attribute Types")

        return report

    def import_attributes(self, attributes):
        report = {"created": [], "updated": [], "failed": [], "changes": []}

        # Start the task with total steps equal to the number of attributes to import
        self.progress_service.start_task(
            "Import Product Attributes", total_steps=len(attributes))

        # Iterate over the list of attributes to process them
        for attribute_data in attributes:
            sku = attribute_data["sku"]
            attribute_type_name = attribute_data["attribute_name"]
            value = attribute_data["value"]

            try:
                # Fetch the product based on SKU
                product = Product.objects.get(sku=sku)
                attribute_type, created = ProductAttributeType.objects.get_or_create(
                    name=attribute_type_name)

                # Check if the attribute type is a slider and if numeric values are involved
                if attribute_type_name in slider_filters:
                    # Extract the numeric value and unit from the provided value
                    new_value, unit = extract_value_and_unit(value)

                    if not unit:
                        # Log the error and skip the creation if unit is missing
                        print(f"Error in unit conversion for attribute '{
                              attribute_type_name}' and value '{value}'.")
                        report["failed"].append(
                            {"sku": sku, "attribute": attribute_type_name, "error": "Unit conversion failed"})
                        continue

                    # Create or update the product attribute
                    product_attribute, created = ProductAttribute.objects.update_or_create(
                        product=product,
                        attribute_type=attribute_type,
                        defaults={"value": new_value, "numeric_value": new_value, "additional_data": {
                            "Unit": unit}},
                    )

                    if created:
                        report["created"].append(
                            {"sku": sku, "attribute": attribute_type_name,
                                "value": new_value, "unit": unit}
                        )
                    else:
                        changes = self.detect_changes(
                            product_attribute, {"value": new_value, "numeric_value": new_value})
                        if changes:
                            report["changes"].append(
                                {"sku": sku, "changes": changes})

                else:
                    # For non-slider (non-numeric) attributes
                    product_attribute, created = ProductAttribute.objects.update_or_create(
                        product=product,
                        attribute_type=attribute_type,
                        defaults={"value": value},
                    )

                    if created:
                        report["created"].append(
                            {"sku": sku, "attribute": attribute_type_name,
                                "value": value}
                        )
                    else:
                        changes = self.detect_changes(
                            product_attribute, {"value": value})
                        if changes:
                            report["changes"].append(
                                {"sku": sku, "changes": changes})

            except Exception as e:
                # Log the error if there's an issue with the product or attribute creation
                print(f"Failed to process Attribute for SKU '{sku}': {str(e)}")
                report["failed"].append(
                    {"sku": sku, "attribute": attribute_type_name,
                        "error": str(e)}
                )

            # Update progress after processing each attribute
            self.progress_service.update_task(
                "Import Product Attributes", steps=1)

        # Complete the task when all attributes are processed
        self.progress_service.complete_task("Import Product Attributes")

        return report

    def update_categories(self, products_data_json):
        print("RealProductCategoryUpdater started...")

        singular_to_plural = {
            "plint": "Plinten",
            "ondervloer": "Ondervloeren",
        }

        MAX_VALUES = 6

        grouped_products = {}
        report = {
            "main_categories_created": [],
            "main_categories_updated": [],
            "subcategories_created": [],
            "sub_subcategories_created": [],
        }

        # Group products by type
        for product in products_data_json:
            product_type = product.get("Type") or product.get("Producttype")
            product_type = singular_to_plural.get(
                product_type.lower(), product_type
            )

            if product_type not in grouped_products:
                grouped_products[product_type] = {
                    "Merk": set(),
                    "Collectie": set(),
                    "Vloertype": set(),
                    "Kleur": set(),
                }

            if product.get("Merk"):
                if len(grouped_products[product_type]["Merk"]) < MAX_VALUES:
                    grouped_products[product_type]["Merk"].add(product["Merk"])

            if product.get("Collectie"):
                if len(grouped_products[product_type]["Collectie"]) < MAX_VALUES:
                    grouped_products[product_type]["Collectie"].add(
                        product["Collectie"]
                    )

            if product.get("Vloertype"):
                if len(grouped_products[product_type]["Vloertype"]) < MAX_VALUES:
                    grouped_products[product_type]["Vloertype"].add(
                        product["Vloertype"]
                    )

            if product.get("Kleur"):
                if len(grouped_products[product_type]["Kleur"]) < MAX_VALUES:
                    grouped_products[product_type]["Kleur"].add(
                        product["Kleur"])

        print(grouped_products)

        # Start the task with total steps based on the categories, subcategories, and sub-subcategories
        # Total for each type of attribute
        total_steps = sum(len(values) for values in grouped_products.values())
        self.progress_service.start_task(
            "Update Categories", total_steps=total_steps)

        # Update or create categories
        for category in category_data:
            category_type = category["name"]
            if category_type in grouped_products and category["for_homepage"] == True:
                for attribute, values in grouped_products[category_type].items():
                    if not values:  # Skip if no values for this header
                        continue

                    subcategories = sorted(list(values))
                    existing_category = ProductCategory.objects.filter(
                        name=category_type
                    ).first()

                    if not existing_category:
                        # Create new category if not exists
                        existing_category = ProductCategory.objects.create(
                            name=category_type,
                            active=category["active"],
                            description=category["description"],
                            thumbnail=category["thumbnail"],
                            for_homepage=category["for_homepage"],
                        )
                        report["main_categories_created"].append(category_type)
                    else:
                        report["main_categories_updated"].append(category_type)

                    for attribute_name in grouped_products[category_type]:
                        if not grouped_products[category_type][attribute_name]:
                            continue

                        subcategory = ProductCategory.objects.filter(
                            name=attribute_name, parent_category=existing_category
                        ).first()
                        if not subcategory:
                            subcategory = ProductCategory.objects.create(
                                name=attribute_name, parent_category=existing_category
                            )
                            report["subcategories_created"].append(
                                attribute_name)

                        for sub_subcategory_name in grouped_products[category_type][attribute_name]:
                            if not ProductCategory.objects.filter(
                                name=sub_subcategory_name, parent_category=subcategory
                            ).exists():
                                ProductCategory.objects.create(
                                    name=sub_subcategory_name, parent_category=subcategory
                                )
                                report["sub_subcategories_created"].append(
                                    sub_subcategory_name
                                )

                        # Update the progress after processing each subcategory/sub-subcategory
                        self.progress_service.update_task(
                            "Update Categories", steps=1)

        # Complete the task after all categories have been processed
        self.progress_service.complete_task("Update Categories")

        print("RealProductCategoryUpdater finished...")
        print("Update Report:")
        print(report)
        return report

    def import_products(self, products):
        report = {
            "created": [],
            "updated": [],
            "failed": [],
            "changes": [],
            "not_updated": [],
            "stock_updated": [],  # Added for tracking stock updates
            "images_updated": [],  # Added for tracking image updates
            "images_failed": [],  # Added for failed image processing
        }

        # Fetch all existing products from the database and extract their SKUs
        existing_skus = set(Product.objects.values_list('sku', flat=True))

        # Create a set of SKUs from the incoming products data
        incoming_skus = {product_data["sku"] for product_data in products}

        # Start the task with total steps equal to the number of products to import
        self.progress_service.start_task(
            "Import Products", total_steps=len(products))

        # Loop over the incoming products
        for product_data in products:
            try:
                product = Product.objects.filter(
                    sku=product_data["sku"]).first()

                if product:
                    # Compare the product with new data to detect changes
                    changes = self.detect_changes(
                        product,
                        {
                            "name": product_data["name"],
                            "supplier": product_data["supplier"],
                            "price": product_data["measure_price"],
                            "unit_price": product_data["unit_price"],
                            "selling_percentage": WebShopConfig().gain_margin(),
                        }
                    )
                    if changes:
                        # If there are changes, update the product
                        Product.objects.filter(sku=product_data["sku"]).update(
                            name=product_data["name"],
                            supplier=product_data["supplier"],
                            price=product_data["measure_price"],
                            unit_price=product_data["unit_price"],
                            selling_percentage=WebShopConfig().gain_margin(),
                        )
                        report["updated"].append(product_data["sku"])
                        report["changes"].append(
                            {"sku": product_data["sku"], "changes": changes})
                    else:
                        print(f"No changes for Product '{product.name}'.")
                else:
                    # If the product does not exist, create a new one
                    product = Product.objects.create(
                        sku=product_data["sku"],
                        name=product_data["name"],
                        supplier=product_data["supplier"],
                        price=product_data["measure_price"],
                        unit_price=product_data["unit_price"],
                        selling_percentage=WebShopConfig().gain_margin(),
                    )
                    print(f"Product '{product.name}' created.")
                    report["created"].append(product_data["sku"])

                # Process product images and stock
                self.handle_product_images(product, product_data, report)
                self.handle_product_stock(product, product_data, report)

            except Exception as e:
                print(f"Failed to process Product '{
                      product_data['sku']}': {str(e)}")
                report["failed"].append(
                    {"sku": product_data["sku"], "error": str(e)})

            # Update progress after processing each product
            self.progress_service.update_task("Import Products", steps=1)

        # After processing all products, check for those that were not updated
        not_updated_skus = existing_skus - incoming_skus

        # Add the SKUs of the products that were not updated to the report
        for sku in not_updated_skus:
            report["not_updated"].append(sku)

        # Complete the task when all products are processed
        self.progress_service.complete_task("Import Products")

        return report

    def handle_product_images(self, product, product_data, report):
        try:
            if "thumbnail" in product_data:
                image_url = product_data["thumbnail"]

                if not product.thumbnail_url or product.thumbnail_url != image_url:
                    product.thumbnail_url = image_url
                    product.save()
                    report["changes"].append(
                        {"sku": product.sku, "field": "thumbnail", "new_value": image_url})
                    print(f"Thumbnail added for product {
                        product.sku}: {image_url}")

            for image_url in product_data.get("images", []):

                # Check if an image with the same filename already exists for this product
                if ProductImage.objects.filter(product=product, image_url=image_url).exists():
                    print(f"Image already exists for product {
                          product.sku}: {image_url}")
                    continue  # Skip saving this image

                 # Create a new ProductImage instance and save the image
                product_image = ProductImage(
                    product=product, image_url=image_url)

                product_image.save()  # Save the ProductImage instance to the database

                report["created"].append(
                    {"sku": product.sku, "image": image_url})

        except Exception as e:
            print(f"Failed to handle images for Product '{
                  product.sku}': {str(e)}")
            report["images_failed"].append(
                {"sku": product.sku, "error": str(e)})

    def handle_product_stock(self, product, product_data, report):
        try:
            stock, created = ProductStock.objects.update_or_create(
                product=product,
                defaults={
                    "quantity": product_data["stock"],
                    "delivery_date": product_data["delivery_date"],
                },
            )
            if created:
                report["stock_updated"].append(
                    {"sku": product.sku, "stock": product_data["stock"]})
            else:
                changes = self.detect_changes(stock, {
                    "quantity": product_data["stock"],
                    "delivery_date": product_data["delivery_date"],
                })
                if changes:
                    report["stock_updated"].append(
                        {"sku": product.sku, "changes": changes})
        except Exception as e:
            print(f"Failed to handle stock for Product '{
                  product.sku}': {str(e)}")
            report["failed"].append({"sku": product.sku, "error": str(e)})

    def update_product_filters(self):
        included_attributes = WebShopConfig.included_filters()
        attributes_for_slider = WebShopConfig.slider_filters()
        categories = ProductCategory.objects.all()
        product_attribute_types = ProductAttributeType.objects.all()

        # Report dictionary to track created and updated filters
        report = {"created": [], "updated": []}

        # Calculate the total number of steps based on the number of categories, attributes, and filters
        # Estimation of total tasks
        total_steps = len(categories) * len(product_attribute_types)
        self.progress_service.start_task(
            "Update Product Filters", total_steps=total_steps)

        for category in categories:
            print("Now in category: ", category)
            for attribute_type in product_attribute_types:
                is_slider = attribute_type.name in attributes_for_slider

                # No excluded attributes and not same name as category
                if attribute_type.name != category.name and attribute_type.name in included_attributes:
                    print("Now in attribute_type: ", attribute_type,
                          "for category: ", category)

                    associated_attributes = ProductAttribute.objects.filter(
                        attribute_type=attribute_type)

                    if category.name == "Zoeken" or category.name == "Assortiment":
                        values_for_filter = []
                        for product_attribute in associated_attributes:
                            if is_slider:
                                try:
                                    numeric_value = float(
                                        product_attribute.numeric_value)
                                except Exception:
                                    numeric_value = None

                                if numeric_value is not None and numeric_value not in values_for_filter:
                                    values_for_filter.append(numeric_value)
                            else:
                                if product_attribute.value not in values_for_filter:
                                    values_for_filter.append(
                                        product_attribute.value)

                        filter_type = "option"

                        if attribute_type.name in attributes_for_slider:
                            filter_type = "slider"

                        # Check if filter already exists, based on name and parent_category
                        existing_filter = ProductFilter.objects.filter(
                            name=attribute_type.name, parent_category=category).first()

                        if existing_filter:
                            # If filter exists, update its values (only add missing ones)
                            existing_values = existing_filter.values
                            added_values = []
                            for value in values_for_filter:
                                if value not in existing_values:
                                    existing_values.append(value)
                                    added_values.append(value)

                            existing_filter.values = existing_values
                            existing_filter.save()

                            if added_values:
                                report["updated"].append({
                                    "filter": existing_filter.name,
                                    "added_values": added_values
                                })
                            print(f"Updated existing filter: {
                                  existing_filter.name}, added values: {added_values}")

                        else:
                            # Create new filter
                            product_filter = ProductFilter.objects.create(
                                name=attribute_type.name,
                                parent_category=category,
                                values=values_for_filter,
                                filter_type=filter_type
                            )

                            report["created"].append({
                                "filter": product_filter.name,
                                "values": values_for_filter
                            })
                            print("Product filter created, with name: ",
                                  product_filter.name)

                    else:
                        product_attributes_with_category = ProductFilterService.filter_attributes_by_category(
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
                                                if numeric_value is not None:
                                                    values_for_filter.append(
                                                        numeric_value)
                                                if unit_value is None:
                                                    unit_value = product_attribute.additional_data["Unit"]
                                            else:
                                                values_for_filter.append(
                                                    product_attribute.value)

                                filter_type = "option"
                                if is_slider:
                                    filter_type = "slider"

                                # Check if filter already exists, based on name and parent_category
                                existing_filter = ProductFilter.objects.filter(
                                    name=attribute_type.name, parent_category=category).first()

                                if existing_filter:
                                    # If filter exists, update its values (only add missing ones)
                                    existing_values = existing_filter.values
                                    added_values = []
                                    for value in values_for_filter:
                                        if value not in existing_values:
                                            existing_values.append(value)
                                            added_values.append(value)

                                    existing_filter.values = existing_values
                                    existing_filter.save()

                                    if added_values:
                                        report["updated"].append({
                                            "filter": existing_filter.name,
                                            "added_values": added_values
                                        })
                                    print(f"Updated existing filter: {
                                          existing_filter.name}, added values: {added_values}")

                                else:
                                    # Create new filter
                                    product_filter = ProductFilter.objects.create(
                                        name=attribute_type.name,
                                        parent_category=category,
                                        values=values_for_filter,
                                        filter_type=filter_type,
                                        unit_value=unit_value
                                    )

                                    report["created"].append({
                                        "filter": product_filter.name,
                                        "values": values_for_filter
                                    })
                                    print(
                                        "Product filter created, with name: ", product_filter.name)

                # Update progress after processing each filter
                self.progress_service.update_task(
                    "Update Product Filters", steps=1)

        # Complete the task after all filters have been processed
        self.progress_service.complete_task("Update Product Filters")

        print("RealProductFilterSeeder finished...")
        return report
