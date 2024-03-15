from django.core.management.base import BaseCommand
from django.db import connection
from ecommerce_website.seeders.product_seeder import ProductSeeder, ProductAttributeTypeSeeder, ProductAttributeSeeder, ProductStockSeeder
from ecommerce_website.models import Product, ProductAttributeType, ProductAttribute, ProductStock


class Command(BaseCommand):
    help = 'Seed initial data into the database'

    def handle(self, *args, **options):

        # Delete existing data
        Product.objects.all().delete()
        ProductAttributeType.objects.all().delete()
        ProductAttribute.objects.all().delete()
        ProductStock.objects.all().delete()

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

        # Seed initial data
        ProductSeeder.seed()
        ProductAttributeTypeSeeder.seed()
        ProductAttributeSeeder.seed()
        ProductStockSeeder.seed()

        self.stdout.write(self.style.SUCCESS('Seed data successfully added'))
