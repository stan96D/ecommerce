from django.core.management.base import BaseCommand
from django.db import connection
from ecommerce_website.seeders.real_seeder import *
from ecommerce_website.models import *


class Command(BaseCommand):
    help = 'Seed initial data into the database'

    def handle(self, *args, **options):

        # Delete existing data
        Product.objects.all().delete()
        ProductSale.objects.all().delete()
        Sale.objects.all().delete()
        ProductAttributeType.objects.all().delete()
        ProductAttribute.objects.all().delete()
        ProductStock.objects.all().delete()
        ProductCategory.objects.all().delete()
        ProductFilter.objects.all().delete()
        Order.objects.all().delete()
        OrderLine.objects.all().delete()
        DeliveryMethod.objects.all().delete()
        StoreMotivation.objects.all().delete()
        StoreRating.objects.all().delete()
        Brand.objects.all().delete()
        ReturnOrderLine.objects.all().delete()
        ReturnOrder.objects.all().delete()

        # Reset primary key sequences for autoincrement fields
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_product';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_productattributetype';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_productattribute';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_productstock';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_productcategory';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_productfilter';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_order';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_orderline';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_productsale';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_deliverymethod';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_sale';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_storemotivation';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_storerating';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_brand';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_returnorderline';")
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='ecommerce_website_returnorder';")

        # Seed initial data
        RealBrandDataSeeder.seed()
        RealDeliveryMethodDataSeeder.seed()
        RealStoreMotivationDataSeeder.seed()
        RealProductDataSeeder.seed()
        # RealProductSaleSeeder.seed()
        RealProductCategorySeeder.seed()
        RealProductFilterSeeder.seed()
        RealStoreRatingDataSeeder.seed()
        RealStoreSeeder.seed()

        self.stdout.write(self.style.SUCCESS('Seed data successfully added'))
