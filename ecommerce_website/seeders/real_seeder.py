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


class RealAddSeederInterface(RealSeederInterface):

    @abstractmethod
    def add(json_data):
        pass


class RealStoreRatingDataSeeder(RealSeederInterface):

    def seed():
        StoreRating.objects.create(
            stars=5,
            title="Geweldige service!",
            description="Ik ben ontzettend tevreden over de service van deze winkel. Snelle levering en de kwaliteit van de producten is top!"
        )

        StoreRating.objects.create(
            stars=4,
            title="Zeer tevreden",
            description="Goede prijs-kwaliteitverhouding en de klantenservice is erg behulpzaam. Enige verbeterpunt zou de levertijd kunnen zijn."
        )

        StoreRating.objects.create(
            stars=3,
            title="Prima winkel, maar...",
            description="De vloeren zijn goedkoop en van goede kwaliteit, maar de bezorging duurde langer dan verwacht. Verder geen klachten."
        )

        StoreRating.objects.create(
            stars=5,
            title="Super snelle levering!",
            description="Mijn vloer was er binnen 48 uur, zoals beloofd. Echt top! De klantenservice was ook erg vriendelijk en behulpzaam."
        )

        StoreRating.objects.create(
            stars=2,
            title="Matige ervaring",
            description="Hoewel de vloeren goedkoop zijn, had ik problemen met de bezorging en het retourneren van producten. Niet helemaal tevreden."
        )

        StoreRating.objects.create(
            stars=4,
            title="Goedkoop en goed",
            description="Voor deze prijs had ik niet zoveel kwaliteit verwacht. De levering was iets vertraagd, maar verder ben ik erg tevreden."
        )

        StoreRating.objects.create(
            stars=5,
            title="Aanrader!",
            description="Ik zou deze winkel zeker aanraden. Uitstekende prijzen, geweldige kwaliteit, en de service is altijd vriendelijk en snel."
        )


class RealStoreMotivationDataSeeder(RealSeederInterface):

    def seed():
        print("RealStoreMotivationDataSeeder started...")

        StoreMotivation.objects.create(name="Top retourservice",
                                       active=True,
                                       text="Is je nieuw gekochte vloer toch niet wat je zoekt? Stuur hem dan gerust kosteloos terug!",
                                       for_homepage=True)

        StoreMotivation.objects.create(name="De beste kwaliteit vloeren",
                                       active=True,
                                       text="Ondanks de goedkope prijs van onze vloeren hebben wij het beste aanbod aan kwaliteitsvloeren. Waar wacht je nog op?",
                                       for_homepage=True)

        StoreMotivation.objects.create(name="De goedkoopste van Nederland en België",
                                       active=True,
                                       text="Wij bieden de goedkoopste vloeren van Nederland en België. Nergens anders krijg je zulke topvloeren voor deze prijs!",
                                       for_homepage=True)

        StoreMotivation.objects.create(name="Binnen 48 uur in huis",
                                       active=True,
                                       text="Door onze geweldige bezorgdienst garanderen wij dat jij je vloer binnen maximaal twee dagen in huis hebt. Leggen maar!",
                                       for_homepage=True)

        print("RealStoreMotivationDataSeeder finished...")


class RealProductDataSeeder(RealAddSeederInterface):

    def seed():
        # with open('ecommerce_website/db_mapper/data/finalized_data2.json', 'r') as file:
        #     json_data_peitsman = json.load(file)

        # database_service = SQLImportService()
        # database_service.import_product_data(json_data_peitsman)

        with open('ecommerce_website/db_mapper/data/finalized_minimal.json', 'r', encoding='utf-8') as file:
            json_data_ppc = json.load(file)

        print("RealProductDataSeeder started...")

        database_service = SQLImportService()
        database_service.import_product_data(json_data_ppc)

        print("RealProductDataSeeder finished...")

    def add(json_data_file):

        with open(json_data_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        print("RealProductDataSeeder started...")

        database_service = SQLImportService()
        database_service.import_product_data(json_data)

        print("RealProductDataSeeder finished...")


class RealDeliveryMethodDataSeeder(RealSeederInterface):

    def seed():
        print("RealDeliveryMethodDataSeeder started...")

        DeliveryMethod.objects.create(name="Bezorging",
                                      price=0.00,
                                      delivery_days=3,
                                      active=True)

        print("RealDeliveryMethodDataSeeder finished...")


class RealBrandDataSeeder(RealSeederInterface):

    def seed():

        print("RealBrandDataSeeder started...")

        Brand.objects.create(name="Beautifloor",
                             image="brand_images/beautifloor_floor.jpg")

        Brand.objects.create(name="Mflor",
                             image="brand_images/mflor_floor.jpg")

        Brand.objects.create(name="Douwes Dekker",
                             image="brand_images/douwers_dekker_floor.jpg")

        Brand.objects.create(name="OTIUM at Home",
                             image="brand_images/otium_floor.jpg")

        Brand.objects.create(name="Sense",
                             image="brand_images/sense_floor.jpg")

        print("RealBrandDataSeeder finished...")


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

# TODO Make this seeder generic based on current data


class RealProductCategorySeeder(RealSeederInterface):
    @staticmethod
    def seed():
        print("RealProductCategorySeeder started...")

        category_data = [
            {
                'name': 'PVC',
                'active': True,
                'for_homepage': True,
                'description': "PVC vloeren",
                'thumbnail': 'category_thumbnails/pvc_category.webp',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Douwes Dekker', 'Sense', 'OTIUM at Home', 'Beautifloor', 'Mflor']
                    },
                    {
                        'name': 'Collectie',
                        'subcategories': ['Shore', 'Fort']
                    },
                    {
                        'name': 'Groef',
                        'subcategories': ['V4 micro', 'V4', 'Geen']
                    },
                    {
                        'name': 'Vloertype',
                        'subcategories': ['Click', 'Dryback']
                    }
                ]
            },
            {
                'name': 'Laminaat',
                'active': True,
                'for_homepage': True,
                'description': "Laminaat vloeren",
                'thumbnail': 'category_thumbnails/laminaat_category.jpg',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Beautifloor', 'Mflor']
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
                'for_homepage': True,
                'description': "Lamelparket vloeren",
                'thumbnail': 'category_thumbnails/lamelparket-category.jpg',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Beautifloor', 'Mflor']
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
                'name': 'Vinyl',
                'active': True,
                'for_homepage': True,
                'description': "Klik Vinyl vloeren",
                'thumbnail': 'category_thumbnails/klik-vinyl-category.jpg',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Beautifloor', 'Mflor']
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
                'name': 'Accessoires',
                'active': True,
                'for_homepage': True,
                'description': "Accessoires om de levensduur van je vloer te vergroten.",
                'thumbnail': 'category_thumbnails/klik-vinyl-category.jpg',
                'subcategories': [
                    {
                        'name': 'Merk',
                        'subcategories': ['Beautifloor', 'Mflor']
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
                'for_homepage': True,
                'description': "De beste vloeren volgens klanten.",
                'thumbnail': 'category_thumbnails/hardlopers_category.jpg',
                'subcategories': [
                ]
            },
            {
                'name': 'Zoeken',
                'active': True,
                'for_homepage': False,
                'description': "Vind de mooiste vloeren bij ons voor de goedkoopste prijs!",
                'thumbnail': None,
                'subcategories': []
            },
            {
                'name': 'Assortiment',
                'active': True,
                'for_homepage': False,
                'description': "Neem een kijkje in ons assortiment. Van PVC tot Laminaat, en Parket tot Visrgaat. Wij hebben het allemaal!",
                'thumbnail': None,
                'subcategories': []
            },
            {
                'name': 'Kortingen',
                'active': True,
                'for_homepage': False,
                'description': "Op zoek naar nog goedkopere vloeren? Zie hier al onze kortingen op de beste vloeren!",
                'thumbnail': None,
                'subcategories': []
            },
        ]

        for category_entry in category_data:
            main_category_name = category_entry['name']
            active = category_entry['active']
            description = category_entry['description']
            thumbnail = category_entry['thumbnail']
            for_homepage = category_entry['for_homepage']

            main_category = ProductCategory.objects.create(
                name=main_category_name, active=active, description=description, thumbnail=thumbnail, for_homepage=for_homepage)

            for subcategory_entry in category_entry['subcategories']:
                subcategory_name = subcategory_entry['name']
                subcategory = ProductCategory.objects.create(
                    name=subcategory_name, parent_category=main_category, active=True)

                for subsubcategory_name in subcategory_entry['subcategories']:
                    ProductCategory.objects.create(
                        name=subsubcategory_name, parent_category=subcategory, active=True)

        print("RealProductCategorySeeder finished...")


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
                        product_attributes_with_category.append(
                            product_attribute)

            else:
                filters = product.attributes.filter(
                    value=category.name)

                if len(filters) > 0:
                    product_attributes_with_category.append(product_attribute)

        return product_attributes_with_category

    @staticmethod
    def seed():
        print("RealProductFilterSeeder started...")

        categories = ProductCategory.objects.all()
        product_attribute_types = ProductAttributeType.objects.all()
        product_filters = {}

        for category in categories:
            print("Now in category: ", category)
            for attribute_type in product_attribute_types:
                print("Now in attribute_type: ", attribute_type,
                      "for category: ", category)

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

                            product_filter.product_attributes.add(
                                product_attribute)

                            product_filters[attribute_type] = product_filter
                else:

                    product_attributes_with_category = []
                    product_attributes_with_category = RealProductFilterSeeder.filter_attributes_by_category(
                        category, associated_attributes)

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
        print("RealProductFilterSeeder finished...")
