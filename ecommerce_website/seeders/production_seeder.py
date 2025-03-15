# Start data
# Store motivations, StoreRatings, Store, DeliveryMethod, Brand(Dynamic foto retrieval), Sale(start), Categoriën(standaard, vullen met data)

# Dynamic data
# Products en ProductFilter


from datetime import datetime, timedelta
from ast import Store
from ecommerce_website.classes.managers.progress_manager.progress_manager import ProgressManager
from ecommerce_website.models import Brand, DeliveryMethod, ProductAttribute, ProductAttributeType, ProductCategory, ProductFilter, StoreMotivation, StoreRating, Sale, Store
from ecommerce_website.services.database_import_service.sql_import_service import SQLImportService
from ecommerce_website.services.product_filter_service.product_filter_service import ProductFilterService
from ecommerce_website.settings.webshop_config import WebShopConfig
from ecommerce_website.seeders.initial_seeder_data.store_ratings import store_ratings
from ecommerce_website.seeders.initial_seeder_data.store_motivations import store_motivations
from ecommerce_website.seeders.initial_seeder_data.category_data import category_data
from ecommerce_website.seeders.initial_seeder_data.brands_data import brands_data
from ecommerce_website.seeders.initial_seeder_data.faq_data import faq_data
from django.db import transaction


class ProductionSeeder():

    def seed_initial(self, products_data_json):
        self.seed_static()

        brands = SQLImportService().import_product_data(products_data_json)

        self.seed_dynamic(products_data_json, brands)
        return

    def seed_static(self):
        self.seed_store()
        self.seed_store_motivation()
        self.seed_delivery_methods()
        self.seed_store_rating()
        self.seed_sale()

    def seed_dynamic(self, products_data_json, brands):
        self.seed_categories(products_data_json)
        self.seed_brands(brands)
        self.seed_product_filters()

    def seed_store(self):
        print("RealStoreSeeder started...")

        Store.objects.create(
            name=WebShopConfig.name(),
            contact_email=WebShopConfig.contact_email(),
            address=WebShopConfig.address(),
            postal_code=WebShopConfig.postal_code(),
            vat_number=WebShopConfig.vat_number(),
            coc_number=WebShopConfig.coc_number(),
            opening_time_week=WebShopConfig.opening_time_week(),
            opening_time_weekend=WebShopConfig.opening_time_weekend(),
            socials=WebShopConfig.socials(),
            faq=faq_data,
            active=True

        )
        print("RealStoreSeeder finished...")

    def seed_store_rating(self):
        print("RealStoreRatingDataSeeder started...")

        for rating in store_ratings:
            StoreRating.objects.create(**rating)

        print("RealStoreRatingDataSeeder finished...")

    def seed_store_motivation(self):
        print("RealStoreMotivationDataSeeder started...")

        for motivation in store_motivations:
            StoreMotivation.objects.create(**motivation)

        print("RealStoreMotivationDataSeeder finished...")

    def seed_delivery_methods(self):
        print("RealDeliveryMethodDataSeeder started...")

        DeliveryMethod.objects.create(name="Bezorging",
                                      price=0.00,
                                      delivery_days=3,
                                      active=True)

        print("RealDeliveryMethodDataSeeder finished...")

    def seed_sale(self):

        Sale.objects.create(
            name="Openingskorting",
            active=True,
            description="Geniet van onze openingskorting!",
            begin_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=60)).date()
        )

    def seed_brands(self, brands):
        for brand_name in brands:
            if brand_name in brands_data:
                Brand.objects.create(
                    name=brand_name, image=brands_data[brand_name])
                print(f"Brand '{brand_name}' created successfully.")
            else:
                print(
                    f"Brand '{brand_name}' not found in mapping. Skipping...")

    def seed_categories(self, products_data_json):
        print("RealProductCategorySeeder started...")

        singular_to_plural = {
            "plint": "Plinten",
            "ondervloer": "Ondervloeren",
        }

        grouped_products = {}

        for product in products_data_json:
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
                grouped_products[product_type]["Merk"].add(product["Merk"])

            if product.get("Collectie"):
                grouped_products[product_type]["Collectie"].add(
                    product["Collectie"])

            if product.get("Vloertype"):
                grouped_products[product_type]["Vloertype"].add(
                    product["Vloertype"])

            if product.get("Kleur"):
                grouped_products[product_type]["Kleur"].add(
                    product["Kleur"])

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

    def seed_product_filters(self):
        progress_manager = ProgressManager()  # Initialize ProgressManager
        included_attributes = WebShopConfig.included_filters()
        attributes_for_slider = WebShopConfig.slider_filters()

        categories = ProductCategory.objects.all()
        product_attribute_types = ProductAttributeType.objects.all()

        total_categories = categories.count()
        total_attribute_types = product_attribute_types.count()

        # Start tracking the overall task
        progress_manager.start_task(
            "Seeding Product Filters", total_steps=total_categories * total_attribute_types)

        # Loop over each category
        for category_index, category in enumerate(categories):
            print("Now in category: ", category)
            # Track progress for categories
            progress_manager.update_task(
                "Seeding Product Filters", steps=total_attribute_types)

            for attribute_type in product_attribute_types:
                print(f"Now processing attribute: {
                      attribute_type.name} for category: {category.name}")

                # Track progress for each category-attribute combination
                progress_manager.update_task(
                    "Seeding Product Filters", steps=1)

                is_slider = attribute_type.name in attributes_for_slider

                # Skip excluded attributes or the ones that have the same name as the category
                if attribute_type.name != category.name and attribute_type.name in included_attributes:

                    print(f"Now in attribute_type: {
                          attribute_type} for category: {category.name}")

                    associated_attributes = ProductAttribute.objects.filter(
                        attribute_type=attribute_type)

                    # Handle filters for "Zoeken" or "Assortiment"
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

                        # Create the product filter
                        product_filter = ProductFilter.objects.create(
                            name=attribute_type.name,
                            parent_category=category,
                            values=values_for_filter,
                            filter_type=filter_type
                        )
                        print(f"Product filter created, with name: {
                              product_filter.name}")
                    else:
                        # Handle other categories
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

                                # Create the product filter
                                product_filter = ProductFilter.objects.create(
                                    name=attribute_type.name,
                                    parent_category=category,
                                    values=values_for_filter,
                                    filter_type=filter_type,
                                    unit_value=unit_value
                                )
                                print(f"Product filter created, with name: {
                                      product_filter.name}")

        # Mark task completion and generate a final report
        progress_manager.complete_task("Seeding Product Filters")
        print("RealProductFilterSeeder finished...")
