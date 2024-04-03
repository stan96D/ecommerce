from django.core.management.base import BaseCommand
from django.db import connection
from ecommerce_website.seeders.product_seeder import ProductSeeder, ProductSaleSeeder, ProductAttributeTypeSeeder, ProductAttributeSeeder, ProductFilterSeeder, ProductStockSeeder, ProductCategorySeeder
from ecommerce_website.models import Product, ProductSale, ProductAttributeType, ProductAttribute, Order, OrderLine, ProductStock, ProductCategory, ProductFilter


class Command(BaseCommand):
    help = 'Seed initial data into the database'

    def handle(self, *args, **options):

        # Delete existing data
        Product.objects.all().delete()
        ProductSale.objects.all().delete()
        ProductAttributeType.objects.all().delete()
        ProductAttribute.objects.all().delete()
        ProductStock.objects.all().delete()
        ProductCategory.objects.all().delete()
        ProductFilter.objects.all().delete()
        Order.objects.all().delete()
        OrderLine.objects.all().delete()

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

        # Seed initial data
        ProductSeeder.seed()
        ProductSaleSeeder.seed()
        ProductAttributeTypeSeeder.seed()
        ProductAttributeSeeder.seed()
        ProductStockSeeder.seed()
        ProductCategorySeeder.seed()
        ProductFilterSeeder.seed()

        self.stdout.write(self.style.SUCCESS('Seed data successfully added'))
