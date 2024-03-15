from ecommerce_website.models import ProductAttribute, ProductAttributeType, Product, ProductStock
from random import randint

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
        attribute_types = ['Artikelnummmer', 'Levereenheid', 'Merk', 'Type', 'Kleur']
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
