from abc import ABC, abstractmethod
import json
from ecommerce_website.services.database_import_service.sql_import_service import SQLImportService
from ecommerce_website.models import *
from random import randint, sample, choice
from django.utils import timezone
from django.db import transaction

class RealSeederInterface(ABC):
    @abstractmethod
    def seed():
        pass

class RealProductDataSeeder(RealSeederInterface):

    def seed():
        with open('ecommerce_website/db_mapper/data/beautifloor.json', 'r') as file:
            json_data = json.load(file)

        database_service = SQLImportService()
        database_service.import_product_data(json_data['products'])


class RealProductSaleSeeder(RealSeederInterface):
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


class RealProductCategorySeeder(RealSeederInterface):
    @staticmethod
    def seed():
        category_data = [
            {
                'name': 'PVC Design',
                'active': True,
                'description': "PVC vloeren",
                'thumbnail': 'category_thumbnails/pvc_category.webp',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Beautifloor']
                    },
                    {
                        'name': 'Collectie',
                        'subcategories': ['Shore', 'Fort']
                    },
                    {
                        'name': 'Groef',
                        'subcategories': ['V4 micro', 'V4', 'Geen']
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
                        'name': 'Merk',
                        'subcategories': ['Beautifloor']
                    },
                    {
                        'name': 'Collectie',
                        'subcategories': ['Antwerpen', 'Anvers']
                    },
                    {
                        'name': 'Groef',
                        'subcategories': ['V4 micro', 'V4', 'Geen']
                    }
                ]
            },
            {
                'name': 'Lamelparket',
                'active': True,
                'description': "Lamerlparket vloeren",
                'thumbnail': 'category_thumbnails/lamelparket-category.jpg',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Beautifloor']
                    },
                    {
                        'name': 'Collectie',
                        'subcategories': ['Miami', 'Boston']
                    },
                    {
                        'name': 'Groef',
                        'subcategories': ['V4 micro', 'V4', 'Geen']
                    }
                ]
            },
            {
                'name': 'Rigid PVC',
                'active': True,
                'description': "Rigid PVC vloeren",
                'thumbnail': 'category_thumbnails/rigid-pvc-category.webp',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Beautifloor']
                    },
                    {
                        'name': 'Collectie',
                        'subcategories': ['Pescado', 'Rios']
                    },
                    {
                        'name': 'Groef',
                        'subcategories': ['V4 micro', 'V4', 'Geen']
                    }
                ]
            },
            {
                'name': 'Klik Vinyl',
                'active': True,
                'description': "Klik Vinyl vloeren",
                'thumbnail': 'category_thumbnails/klik-vinyl-category.jpg',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Beautifloor']
                    },
                    {
                        'name': 'Collectie',
                        'subcategories': ['Laghi', 'Citta']
                    },
                    {
                        'name': 'Groef',
                        'subcategories': ['V4 micro', 'V4', 'Geen']
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


class RealProductFilterSeeder(RealSeederInterface):

    @staticmethod
    def filter_attributes_by_category(category, product_attributes):
        product_attributes_with_category = []

        for product_attribute in product_attributes:
            product = product_attribute.product

            if category.parent_category:

                if category.parent_category.parent_category:

                    main_filter = product.attributes.filter(
                        value=category.parent_category.parent_category.name)

                    sub_filter = product.attributes.filter(
                        attribute_type__name=category.parent_category.name)
                    
                    last_filter = product.attributes.filter(
                        value=category.name)

                    if len(sub_filter) > 0 and len(main_filter) > 0 and len(last_filter) > 0:
                        product_attributes_with_category.append(
                            product_attribute)
                else:

                    main_filter = product.attributes.filter(
                        value=category.parent_category.name)
                    
                    sub_filter = product.attributes.filter(
                        attribute_type__name=category.name)

                    if len(sub_filter) > 0 and len(main_filter) > 0:
                        product_attributes_with_category.append(product_attribute)


            else:
                filters = product.attributes.filter(
                    value=category.name)
                            
                if len(filters) > 0:
                    product_attributes_with_category.append(product_attribute)


        return product_attributes_with_category

    @staticmethod
    def seed():
        categories = ProductCategory.objects.all()
        product_attribute_types = ProductAttributeType.objects.all()
        product_filters = {}

        for category in categories:

            for attribute_type in product_attribute_types:

                associated_attributes = ProductAttribute.objects.filter(
                    attribute_type=attribute_type)

                if category.name == "Zoeken":

                    for product_attribute in associated_attributes:

                        if attribute_type in product_filters:

                            filter = product_filters[attribute_type]

                            if len(filter.product_attributes.filter(value=product_attribute.value)) == 0:
                                product_filters[attribute_type].product_attributes.add(
                                product_attribute)
                        else:
                            product_filter = ProductFilter.objects.create(
                                name=attribute_type, parent_category=category)

                            product_filter.product_attributes.add(product_attribute)

                            product_filters[attribute_type] = product_filter
                else:

                    product_attributes_with_category = []
                    product_attributes_with_category = RealProductFilterSeeder.filter_attributes_by_category(category, associated_attributes)


                    if len(product_attributes_with_category) > 0:

                        with transaction.atomic():
                            product_filter = ProductFilter.objects.create(
                                            name=attribute_type.name,
                                            parent_category=category
                                        )

                            for product_attribute in product_attributes_with_category:
                                if attribute_type.id == product_attribute.attribute_type.id:
                                    if not product_filter.product_attributes.filter(value=product_attribute.value).exists():
                                        product_filter.product_attributes.add(
                                                        product_attribute)




