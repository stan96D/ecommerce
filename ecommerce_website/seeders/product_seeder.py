from ecommerce_website.models import ProductAttribute, ProductAttributeType, Product, ProductStock, ProductCategory, ProductCategoryAttribute
from random import randint, sample
from django.db import transaction

class ProductSeeder:
    @staticmethod
    def seed():
        products_data = [
            {'name': 'Classen Skyline Sonolta Eiken Laminaat 56179',
                'price': 16.95, 'thumbnail': 'thumbnails/vloer1.jpg'},
            {'name': 'Meister Lindura HD 400-270 8923 Eik Authentic Greige',
                'price': 79.15, 'thumbnail': 'thumbnails/vloer2.jpg'},
        ]
        for data in products_data:
            Product.objects.create(**data)


class ProductAttributeTypeSeeder:
    @staticmethod
    def seed():
        attribute_types = ['Artikelnummer', 'Levereenheid', 'Merk', 'Type', 'Kleur']
        for name in attribute_types:
            ProductAttributeType.objects.create(name=name)


class ProductAttributeSeeder:
    @staticmethod
    def seed():
        product_attributes_data = [
            {'product_id': 1, 'attribute_type_id': 1, 'value': '4828'},
            {'product_id': 1, 'attribute_type_id': 2, 'value': '2.22'},
            {'product_id': 1, 'attribute_type_id': 3, 'value': 'Classen Skyline'},
            {'product_id': 1, 'attribute_type_id': 4, 'value': 'Laminaat'},

            {'product_id': 2, 'attribute_type_id': 1, 'value': '8439'},
            {'product_id': 2, 'attribute_type_id': 2, 'value': '2.46'},
            {'product_id': 2, 'attribute_type_id': 3, 'value': 'Meister Lindura'},
            {'product_id': 2, 'attribute_type_id': 4, 'value': 'PVC'},

        ]
        for data in product_attributes_data:
            ProductAttribute.objects.create(**data)


class ProductStockSeeder:
    @staticmethod
    def seed():
        products = Product.objects.all()
        for product in products:
            quantity = randint(0, 100)
            ProductStock.objects.create(product=product, quantity=quantity)


class ProductCategorySeeder:
    @staticmethod
    def seed():
        category_names = ['PVC', 'Laminaat', 'Hout',
                          'Plinten en Profielen', 'Accessoires']

        for name in category_names:
            ProductCategory.objects.create(name=name)


class ProductCategoryAttributeSeeder:
    @staticmethod
    def seed():
        attribute_types = ProductAttributeType.objects.filter(id__range=(3, 5))

        for category in ProductCategory.objects.all():
            with transaction.atomic():
                for attribute_type in attribute_types:  
                    category_attribute = ProductCategoryAttribute.objects.create(
                        category=category, attribute_type=attribute_type)

                    product_attributes = ProductAttribute.objects.filter(
                        attribute_type=attribute_type)
                    selected_attributes = sample(
                        list(product_attributes), min(3, len(product_attributes)))
                    category_attribute.attributes.add(*selected_attributes)

        