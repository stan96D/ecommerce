from abc import ABC, abstractmethod
from decimal import Decimal
import json
import re
from ecommerce_website.classes.helpers.numeric_value_normalizer import extract_lowest_and_highest
from ecommerce_website.services.database_import_service.sql_import_service import SQLImportService
from ecommerce_website.models import *
from random import randint, sample, choice
from django.utils import timezone
from django.db import transaction
from ecommerce_website.settings.webshop_config import WebShopConfig


class RealSeederInterface(ABC):
    @abstractmethod
    def seed():
        pass


class RealAddSeederInterface(RealSeederInterface):

    @abstractmethod
    def add(json_data):
        pass


class RealStoreSeeder(RealSeederInterface):

    def seed():
        print("RealStoreSeeder started...")

        Store.objects.create(
            contact_email=WebShopConfig.contact_email(),
            address=WebShopConfig.address(),
            postal_code=WebShopConfig.postal_code(),
            vat_number=WebShopConfig.vat_number(),
            coc_number=WebShopConfig.coc_number(),
            opening_time_week=WebShopConfig.opening_time_week(),
            opening_time_weekend=WebShopConfig.opening_time_weekend(),
            active=True

        )
        print("RealStoreSeeder finished...")


class RealStoreRatingDataSeeder(RealSeederInterface):

    def seed():

        print("RealStoreRatingDataSeeder started...")

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
            description="Mijn vloer was er binnen 96 uur, zoals beloofd. Echt top! De klantenservice was ook erg vriendelijk en behulpzaam."
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

        print("RealStoreRatingDataSeeder finished...")


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

        StoreMotivation.objects.create(name="Binnen 96 uur in huis",
                                       active=True,
                                       text="Door onze geweldige bezorgdienst garanderen wij dat jij je vloer binnen maximaal vier (werk)dagen in huis hebt. Leggen maar!",
                                       for_homepage=True)

        print("RealStoreMotivationDataSeeder finished...")


class RealProductDataSeeder(RealAddSeederInterface):

    def seed():
        print("RealProductDataSeeder started...")

        with open('ecommerce_website/db_mapper/data/final_data/finalized_combined.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        database_service = SQLImportService()
        database_service.import_product_data(json_data)

        # with open('ecommerce_website/db_mapper/data/finalized_minimal.json', 'r', encoding='utf-8') as file:
        #     json_data_ppc = json.load(file)

        # database_service = SQLImportService()
        # database_service.import_product_data(json_data_ppc)

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
                             image="brand_images/douwes_dekker_floor.jpg")

        Brand.objects.create(name="OTIUM at Home",
                             image="brand_images/otium_floor.jpg")

        Brand.objects.create(name="Sense",
                             image="brand_images/sense_floor.jpeg")

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

        with open('ecommerce_website/db_mapper/data/final_data/finalized_combined.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        singular_to_plural = {
            "plint": "Plinten",
            "ondervloer": "Ondervloeren",
        }

        MAX_VALUES = 6

        grouped_products = {}

        for product in json_data:
            product_type = product.get("Type") or product.get("Producttype")
            product_type = singular_to_plural.get(
                product_type.lower(), product_type)

            if product_type not in grouped_products:
                grouped_products[product_type] = {
                    "Merk": set(),
                    "Collectie": set(),
                    "Vloertype": set(),
                    "Kleur": set()
                }

            if product.get("Merk"):
                if len(grouped_products[product_type]["Merk"]) < MAX_VALUES:
                    grouped_products[product_type]["Merk"].add(product["Merk"])

            if product.get("Collectie"):
                if len(grouped_products[product_type]["Collectie"]) < MAX_VALUES:
                    grouped_products[product_type]["Collectie"].add(
                        product["Collectie"])

            if product.get("Vloertype"):
                if len(grouped_products[product_type]["Vloertype"]) < MAX_VALUES:
                    grouped_products[product_type]["Vloertype"].add(
                        product["Vloertype"])

            if product.get("Kleur"):
                if len(grouped_products[product_type]["Kleur"]) < MAX_VALUES:
                    grouped_products[product_type]["Kleur"].add(
                        product["Kleur"])

        category_data = [
            {
                'name': 'PVC',
                'active': True,
                'for_homepage': True,
                'description': "PVC vloeren",
                'thumbnail': 'category_thumbnails/pvc_category.webp',
                'subcategories': [

                ]
            },
            {
                'name': 'Laminaat',
                'active': True,
                'for_homepage': True,
                'description': "Laminaat vloeren",
                'thumbnail': 'category_thumbnails/laminaat_category.jpg',
                'subcategories': [

                ]
            },
            {
                'name': 'Lamelparket',
                'active': True,
                'for_homepage': True,
                'description': "Lamelparket vloeren",
                'thumbnail': 'category_thumbnails/lamelparket-category.jpg',
                'subcategories': [

                ]
            },
            {
                'name': 'Vinyl',
                'active': True,
                'for_homepage': True,
                'description': "Klik Vinyl vloeren",
                'thumbnail': 'category_thumbnails/klik-vinyl-category.jpg',
                'subcategories': [

                ]
            },

            {
                'name': 'Plinten',
                'active': True,
                'for_homepage': True,
                'description': "Accessoires om de levensduur van je vloer te vergroten.",
                'thumbnail': 'category_thumbnails/klik-vinyl-category.jpg',
                'subcategories': [

                ]
            },
            {
                'name': 'Ondervloeren',
                'active': True,
                'for_homepage': True,
                'description': "Accessoires om de levensduur van je vloer te vergroten.",
                'thumbnail': 'category_thumbnails/klik-vinyl-category.jpg',
                'subcategories': [
                ]
            },
            {
                'name': 'Hardlopers',
                'active': True,
                'for_homepage': False,
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

        print(grouped_products)
        for category in category_data:
            # Match this with 'Type' or 'Producttype'
            category_type = category['name']
            if category_type in grouped_products and category['for_homepage'] == True:
                for attribute, values in grouped_products[category_type].items():
                    if values:  # Only add if there are values
                        category['subcategories'].append({
                            'name': attribute,
                            # Sort values alphabetically
                            'subcategories': sorted(list(values))
                        })

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

        excluded_attributes = WebShopConfig.excluded_filters()

        attributes_for_slider = WebShopConfig.slider_filters()

        categories = ProductCategory.objects.all()
        product_attribute_types = ProductAttributeType.objects.all()

        for category in categories:
            print("Now in category: ", category)
            for attribute_type in product_attribute_types:

                is_slider = attribute_type.name in attributes_for_slider

                # No excluded attributes and not same name as category
                if attribute_type.name != category.name and attribute_type.name not in excluded_attributes:

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
                                print("numeric", numeric_value)
                                if numeric_value is not None:
                                    values_for_filter.append(
                                        numeric_value)
                            else:
                                values_for_filter.append(
                                    product_attribute.value)

                        filter_type = "option"

                        if attribute_type.name in attributes_for_slider:
                            filter_type = "slider"

                        product_filter = ProductFilter.objects.create(
                            name=attribute_type.name,
                            parent_category=category,
                            values=values_for_filter,
                            filter_type=filter_type
                        )
                        print("Product filter created, with name: ",
                              product_filter.name)

                    else:

                        product_attributes_with_category = []
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

                                filter_type = "option"

                                if is_slider:
                                    filter_type = "slider"

                                product_filter = ProductFilter.objects.create(
                                    name=attribute_type.name,
                                    parent_category=category,
                                    values=values_for_filter,
                                    filter_type=filter_type,
                                    unit_value=unit_value

                                )
                                print("Product filter created, with name: ",
                                      product_filter.name)

        print("RealProductFilterSeeder finished...")
