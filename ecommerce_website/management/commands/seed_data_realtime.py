from django.core.management.base import BaseCommand
from ecommerce_website.db_mapper.sql_db_mapper import SQLDatabaseMapper
import json
from ecommerce_website.models import *
from ecommerce_website.db_mapper.base_db_mapper import DatabaseMapperInterface
from ecommerce_website.db_mapper.data import *
import requests
from django.core.files import File
from io import BytesIO


class Command(BaseCommand):
    help = 'Execute SQLDatabaseMapper script'

    def handle(self, *args, **options):
        
        with open('ecommerce_website/db_mapper/data/beautifloor.json', 'r') as file:
            json_data = json.load(file)

        # print(json_data)  

        mapper = SQLDatabaseMapper()

        products, attributes, types = mapper.map_products(json_data['products'])

        for type_data in types:
            try:
                product_attribute_type = ProductAttributeType.objects.get(
                    name=type_data["name"])
                print(f"ProductAttributeType '{ product_attribute_type.name}' already exists.")
            except ProductAttributeType.DoesNotExist:
                product_attribute_type = ProductAttributeType.objects.create(
                    name=type_data["name"])
                print(f"ProductAttributeType '{product_attribute_type.name}' created.")
        
        
        for product in products:
            try:
                product = Product.objects.get(
                    name=product["name"])
                print(f"Product '{product.name}' already exists.")
            except Product.DoesNotExist:
                image_url = product['thumbnail']
                response = requests.get(image_url)


                product = Product.objects.create(
                    name=product["name"])
                
                if response.status_code == 200:
                    image_name = image_url.split('/')[-1]
                    image_bytes = BytesIO(response.content)
                    product.thumbnail.save(image_name, File(image_bytes))
                quantity = 0
                ProductStock.objects.create(product=product, quantity=quantity)
                print(f"Product '{product.name}' created.")


        for attribute_data in attributes:
            product_name = attribute_data['product_name']
            attribute_type_name = attribute_data['attribute_name']
            value = attribute_data['value']

            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                print(f"Product '{product_name}' does not exist.")
            else:
                try:
                    attribute_type = ProductAttributeType.objects.get(
                        name=attribute_type_name)
                except ProductAttributeType.DoesNotExist:
                    print(f"ProductAttributeType '{attribute_type_name}' does not exist.")
                else:
                    if ProductAttribute.objects.filter(product=product, attribute_type=attribute_type, value=value).exists():
                        print(f"ProductAttribute with product '{product_name}', attribute type '{ attribute_type_name}', and value '{value}' already exists.")
                    else:
                        product_attribute = ProductAttribute.objects.create(
                            product=product,
                            attribute_type=attribute_type,
                            value=value
                        )
                        print(f"ProductAttribute '{product_attribute}' created.")



