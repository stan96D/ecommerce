from ecommerce_website.services.database_import_service.base_database_import_service import DatabaseImportServiceInterface
from ecommerce_website.db_mapper.sql_db_mapper import SQLDatabaseMapper
from ecommerce_website.models import *
from ecommerce_website.db_mapper.data import *
import requests
from django.core.files import File
from io import BytesIO

import requests
from io import BytesIO
from django.core.files import File
from ecommerce_website.settings.webshop_config import *

class SQLImportService(DatabaseImportServiceInterface):
    def import_product_data(self, json):

        mapper = SQLDatabaseMapper()

        products, attributes, types = mapper.map_products(
            json)

        self.import_product_attribute_types(types)
        self.import_products(products)
        self.import_attributes(attributes)

    def import_product_attribute_types(self, types):
        for type_data in types:
            try:
                product_attribute_type = ProductAttributeType.objects.get(
                    name=type_data["name"])
                print(f"ProductAttributeType '{product_attribute_type.name}' already exists.")
            except ProductAttributeType.DoesNotExist:
                product_attribute_type = ProductAttributeType.objects.create(
                    name=type_data["name"])
                print(f"ProductAttributeType '{product_attribute_type.name}' created.")

    def import_products(self, products):
        for product in products:
            try:
                product = Product.objects.get(name=product["name"])
                print(f"Product '{product.name}' already exists.")
            except Product.DoesNotExist:
                self.create_product(product)

    def create_product(self, product_data):
        image_url = product_data['thumbnail']
        response = requests.get(image_url)

        config = WebShopConfig()
        selling_percentage = config.selling_percentage

        product = Product.objects.create(
            name=product_data["name"], price=product_data["measure_price"], unit_price=product_data["unit_price"], selling_percentage=selling_percentage)

        if response.status_code == 200:
            image_name = image_url.split('/')[-1]
            image_bytes = BytesIO(response.content)
            product.thumbnail.save(image_name, File(image_bytes))

        ProductStock.objects.create(product=product, quantity=100)

        for image_url in product_data.get('images', []):
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_name = image_url.split('/')[-1]
                image_bytes = BytesIO(image_response.content)
                product_image = ProductImage(product=product)
                product_image.image.save(image_name, File(image_bytes))
                product_image.save()

        print(f"Product '{product.name}' created.")

    def import_attributes(self, attributes):
        for attribute_data in attributes:
            product_name = attribute_data['product_name']
            attribute_type_name = attribute_data['attribute_name']
            value = attribute_data['value']

            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                print(f"Product '{product_name}' does not exist.")
            else:
                self.create_product_attribute(
                    product, attribute_type_name, value)

    def create_product_attribute(self, product, attribute_type_name, value):
        try:
            attribute_type = ProductAttributeType.objects.get(
                name=attribute_type_name)
        except ProductAttributeType.DoesNotExist:
            print(f"ProductAttributeType '{attribute_type_name}' does not exist.")
        else:
            if not ProductAttribute.objects.filter(product=product, attribute_type=attribute_type, value=value).exists():
                product_attribute = ProductAttribute.objects.create(
                    product=product,
                    attribute_type=attribute_type,
                    value=value
                )
                print(f"ProductAttribute '{product_attribute}' created.")
            else:
                print(f"ProductAttribute with product '{product.name}', attribute type '{attribute_type_name}', and value '{value}' already exists.")
