from ecommerce_website.models import ProductAttribute, ProductSale, ProductAttributeType, Product, ProductStock, ProductCategory, ProductFilter
from random import randint, sample, choice
from django.db import transaction
from django.utils import timezone

class ProductSeeder:
    @staticmethod
    def seed():
        products_data = [
            {'name': 'Classen Skyline Sonolta Eiken Laminaat 56179',
             'price': 16.95, 'thumbnail': 'product_thumbnails/vloer1.jpg'},
            {'name': 'Meister Lindura HD 400-270 8923 Eik Authentic Greige',
             'price': 79.15, 'thumbnail': 'product_thumbnails/vloer2.jpg'},
            {'name': 'Quick-Step Impressive Ultra IMU1859',
             'price': 49.99, 'thumbnail': 'product_thumbnails/vloer3.jpg'},
            {'name': 'Pergo Sensation Authentiek Laminaat - Donker Eiken',
             'price': 69.99, 'thumbnail': 'product_thumbnails/vloer4.jpg'},
            {'name': 'BerryAlloc Spirit - Eik Blond',
             'price': 54.50, 'thumbnail': 'product_thumbnails/vloer5.jpg', 'runner': True},
            {'name': 'Kronotex Mammut Plus - Zilver Eik',
             'price': 59.75, 'thumbnail': 'product_thumbnails/vloer6.jpg', 'runner': True},
            {'name': 'Egger Kingsize V4 - Wit Eiken',
             'price': 45.80, 'thumbnail': 'product_thumbnails/vloer7.jpg', 'runner': True},
            {'name': 'Balterio Grande Wide - Vintage Eik',
             'price': 65.25, 'thumbnail': 'product_thumbnails/vloer8.jpg', 'runner': True},
        ]

        for data in products_data:
            Product.objects.create(**data)


class ProductSaleSeeder:
    @staticmethod
    def seed():
        products = Product.objects.filter()
        for product in products:
            if not ProductSale.objects.filter(product=product).exists():
                if randint(1, 10) <= 3:
                    active = choice([True, False])
                    percentage = randint(5, 50)
                    dealname = f"Spring Sale - {percentage}% Off"
                    begin_date = timezone.now()
                    end_date = begin_date + timezone.timedelta(days=30)

                    ProductSale.objects.create(
                        product=product,
                        active=active,
                        percentage=percentage,
                        dealname=dealname,
                        begin_date=begin_date,
                        end_date=end_date
                    )


class ProductAttributeTypeSeeder:
    @staticmethod
    def seed():
        attribute_types = ['Artikelnummer', 'Levereenheid', 'Type', 'Merk', 'Kleur']
        for name in attribute_types:
            ProductAttributeType.objects.create(name=name)


class ProductAttributeSeeder:
    @staticmethod
    def seed():
        product_attributes_data = [
            {'product_id': 1, 'attribute_type_id': 1, 'value': '4828'},
            {'product_id': 1, 'attribute_type_id': 2, 'value': '2.22'},
            {'product_id': 1, 'attribute_type_id': 4, 'value': 'Classen Skyline'},
            {'product_id': 1, 'attribute_type_id': 3, 'value': 'Laminaat'},
            {'product_id': 1, 'attribute_type_id': 5,
                'value': 'Grey'}, 

            {'product_id': 2, 'attribute_type_id': 1, 'value': '8439'},
            {'product_id': 2, 'attribute_type_id': 2, 'value': '2.46'},
            {'product_id': 2, 'attribute_type_id': 4, 'value': 'Meister Lindura'},
            {'product_id': 2, 'attribute_type_id': 3, 'value': 'PVC'},
            {'product_id': 2, 'attribute_type_id': 5,
                'value': 'White'}, 

            {'product_id': 3, 'attribute_type_id': 1, 'value': '9251'},
            {'product_id': 3, 'attribute_type_id': 2, 'value': '3.10'},
            {'product_id': 3, 'attribute_type_id': 4,
                'value': 'Quick-Step Impressive Ultra'},
            {'product_id': 3, 'attribute_type_id': 3, 'value': 'Laminaat'},
            {'product_id': 3, 'attribute_type_id': 5,
                'value': 'White'},  

            {'product_id': 4, 'attribute_type_id': 1, 'value': '7392'},
            {'product_id': 4, 'attribute_type_id': 2, 'value': '2.85'},
            {'product_id': 4, 'attribute_type_id': 4, 'value': 'Pergo Sensation'},
            {'product_id': 4, 'attribute_type_id': 3, 'value': 'Laminaat'},
            {'product_id': 4, 'attribute_type_id': 5,
                'value': 'Brown'}, 

            {'product_id': 5, 'attribute_type_id': 1, 'value': '6318'},
            {'product_id': 5, 'attribute_type_id': 2, 'value': '2.30'},
            {'product_id': 5, 'attribute_type_id': 4, 'value': 'BerryAlloc Spirit'},
            {'product_id': 5, 'attribute_type_id': 3, 'value': 'Laminaat'},
            {'product_id': 5, 'attribute_type_id': 5,
                'value': 'Brown'},  

            {'product_id': 6, 'attribute_type_id': 1, 'value': '8472'},
            {'product_id': 6, 'attribute_type_id': 2, 'value': '2.65'},
            {'product_id': 6, 'attribute_type_id': 4,
                'value': 'Kronotex Mammut Plus'},
            {'product_id': 6, 'attribute_type_id': 3, 'value': 'Laminaat'},
            {'product_id': 6, 'attribute_type_id': 5,
                'value': 'White'}, 

            {'product_id': 7, 'attribute_type_id': 1, 'value': '2135'},
            {'product_id': 7, 'attribute_type_id': 2, 'value': '3.40'},
            {'product_id': 7, 'attribute_type_id': 4, 'value': 'Egger Kingsize V4'},
            {'product_id': 7, 'attribute_type_id': 3, 'value': 'Laminaat'},
            {'product_id': 7, 'attribute_type_id': 5,
                'value': 'Grey'},  

            {'product_id': 8, 'attribute_type_id': 1, 'value': '4991'},
            {'product_id': 8, 'attribute_type_id': 2, 'value': '3.15'},
            {'product_id': 8, 'attribute_type_id': 4,
                'value': 'Balterio Grande Wide'},
            {'product_id': 8, 'attribute_type_id': 3, 'value': 'Laminaat'},
            {'product_id': 8, 'attribute_type_id': 5,
                'value': 'Brown'},  

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
        category_data = [
            {
                'name': 'PVC',
                'active': True,
                'description': "PVC vloeren",
                'thumbnail': 'category_thumbnails/pvc_category.webp',
                'subcategories': [
                    {
                        'name': 'Kleur',
                        'subcategories': ['White', 'Grey', 'Brown']
                    },
                    {
                        'name': 'Merk',
                        'subcategories': ['Classen Skyline', 'Meister Lindura', 'Pergo Sensation']
                    }
                ]
            },
            {
                'name': 'Laminaat',
                'active': True,
                'description': "Laminaat vloeren",
                'thumbnail': 'category_thumbnails/laminaat_category.jpg',
                'subcategories': [
                    {
                        'name': 'Kleur',
                        'subcategories': ['White', 'Grey', 'Brown']
                    },
                    {
                        'name': 'Merk',
                        'subcategories': ['Classen Skyline', 'Meister Lindura', 'Pergo Sensation']
                    }
                ]
            },
            {
                'name': 'Hardlopers',
                'active': True,
                'description': "De beste vloeren volgens klanten.",
                'thumbnail': 'category_thumbnails/hardlopers_category.jpg',
                'subcategories': [
                ]
            },
            {
                'name': 'Zoeken',
                'active': False,
                'description': "Vind de mooiste vloeren bij ons voor de goedkoopste prijs!",
                'thumbnail': None,
                'subcategories': []
            }
        ]

        for category_entry in category_data:
            main_category_name = category_entry['name']
            active = category_entry['active']
            description = category_entry['description']
            thumbnail = category_entry['thumbnail']

            main_category = ProductCategory.objects.create(
                name=main_category_name, active=active, description=description, thumbnail=thumbnail)

            for subcategory_entry in category_entry['subcategories']:
                subcategory_name = subcategory_entry['name']
                subcategory = ProductCategory.objects.create(
                    name=subcategory_name, parent_category=main_category, active=True)

                for subsubcategory_name in subcategory_entry['subcategories']:
                    ProductCategory.objects.create(
                        name=subsubcategory_name, parent_category=subcategory, active=True)



class ProductFilterSeeder:
    @staticmethod
    def seed():
        categories = ProductCategory.objects.all()
        product_attributes = ProductAttribute.objects.all()
        product_attribute_types = ProductAttributeType.objects.all()
        for category in categories:

            for attribute_type in product_attribute_types:

                with transaction.atomic():
                    product_filter = ProductFilter.objects.create(
                        name=attribute_type.name,
                        parent_category=category
                    )

                    for product_attribute in product_attributes:
                        if attribute_type.id == product_attribute.attribute_type.id:
                            if not product_filter.product_attributes.filter(value=product_attribute.value).exists():
                                product_filter.product_attributes.add(product_attribute)










        