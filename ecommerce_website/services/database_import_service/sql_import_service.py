import logging
import time
from ecommerce_website.services.database_import_service.base_database_import_service import DatabaseImportServiceInterface
from ecommerce_website.db_mapper.sql_db_mapper import SQLDatabaseMapper
from ecommerce_website.models import *
from ecommerce_website.db_mapper.data import *
from ecommerce_website.settings.webshop_config import *
from ecommerce_website.classes.helpers.numeric_value_normalizer import extract_value_and_unit
from ecommerce_website.classes.managers.progress_manager.progress_manager import ProgressManager

slider_filters = WebShopConfig.slider_filters()
logger = logging.getLogger(__name__)


class SQLImportService(DatabaseImportServiceInterface):
    def __init__(self):
        self.progress_manager = ProgressManager()

    def import_product_data(self, json):
        mapper = SQLDatabaseMapper()
        products, attributes, types = mapper.map_products(json)

        # Start tracking progress for product import
        self.progress_manager.start_task(
            'import_product_attribute_types', total_steps=len(types))
        self.import_product_attribute_types(types)
        self.progress_manager.start_task(
            'import_products', total_steps=len(products))
        self.import_products(products)

        # Start tracking progress for attribute import
        self.progress_manager.start_task(
            'import_attributes', total_steps=len(attributes))
        return self.import_attributes(attributes)

    def import_product_attribute_types(self, types):
        for type_data in types:
            try:
                product_attribute_type = ProductAttributeType.objects.get(
                    name=type_data["name"])
                print(f"ProductAttributeType '{
                      product_attribute_type.name}' already exists.")
            except ProductAttributeType.DoesNotExist:
                product_attribute_type = ProductAttributeType.objects.create(
                    name=type_data["name"])
                print(f"ProductAttributeType '{
                      product_attribute_type.name}' created.")

    def import_products(self, products):
        for product in products:
            try:
                product = Product.objects.get(sku=product["sku"])
                print(f"Product '{product.name}' already exists.")
            except Product.DoesNotExist:
                self.create_product(product)

            # Update the progress of product import after each product is processed
            self.progress_manager.update_task('import_products', steps=1)

        # Mark the task as completed once all products are imported
        self.progress_manager.complete_task('import_products')

    def create_product(self, product_data):
        start_time = time.time()
        logger.info(f"Creating product: {
            product_data['name']} (SKU: {product_data['sku']})")

        image_url = product_data['thumbnail']

        config = WebShopConfig()
        selling_percentage = config.gain_margin()

        # Create product object
        product = Product.objects.create(
            name=product_data["name"],
            supplier=product_data["supplier"],
            sku=product_data["sku"],
            price=product_data["measure_price"],
            unit_price=product_data["unit_price"],
            thumbnail_url=product_data['thumbnail'],
            selling_percentage=selling_percentage
            )
        logger.info(f"Product '{product.name}' created successfully.")

        # Create the product stock record
        ProductStock.objects.create(
                product=product,
                quantity=product_data["stock"],
                delivery_date=product_data["delivery_date"]
            )
        logger.info(f"Stock for product '{product.name}' added successfully.")

        # Handle additional product images
        for image_url in product_data.get('images', []):

                    product_image = ProductImage(
                        product=product,
                        image_url=image_url
                    )
                    product_image.save()

        # Calculate and log time taken to create the product
        elapsed_time = time.time() - start_time
        logger.info(f"Product '{product.name}' creation completed in {
                        elapsed_time:.2f} seconds.")

    def import_attributes(self, attributes):
        all_brands = set()

        for attribute_data in attributes:
            sku = attribute_data['sku']
            attribute_type_name = attribute_data['attribute_name']
            value = attribute_data['value']

            if attribute_type_name == "Merk":
                all_brands.add(value)

            try:
                product = Product.objects.get(sku=sku)
            except Product.DoesNotExist:
                print(f"Product '{sku}' does not exist.")
            else:
                self.create_product_attribute(
                    product, attribute_type_name, value)

            # Update the progress after each attribute is processed
            self.progress_manager.update_task('import_attributes', steps=1)

        # Mark the task as completed once all attributes are imported
        self.progress_manager.complete_task('import_attributes')

        return all_brands

    def create_product_attribute(self, product, attribute_type_name, value):
        try:
            attribute_type = ProductAttributeType.objects.get(
                name=attribute_type_name)
        except ProductAttributeType.DoesNotExist:
            print(f"ProductAttributeType '{
                  attribute_type_name}' does not exist.")
        else:
            if not ProductAttribute.objects.filter(product=product, attribute_type=attribute_type, value=value).exists():
                if attribute_type.name in slider_filters:
                    new_value, unit = extract_value_and_unit(value)
                    if not unit:
                        print(
                            "ProductAttribute not created error in unit conversion for additional data UNIT....")
                        return

                    product_attribute = ProductAttribute.objects.create(
                        product=product,
                        attribute_type=attribute_type,
                        value=new_value,
                        numeric_value=new_value,
                        additional_data={"Unit": unit}
                    )

                else:
                    product_attribute = ProductAttribute.objects.create(
                        product=product,
                        attribute_type=attribute_type,
                        value=value
                    )

                print(f"ProductAttribute '{product_attribute}' created.")
            else:
                print(f"ProductAttribute with product '{product.name}', attribute type '{
                      attribute_type_name}', and value '{value}' already exists.")
