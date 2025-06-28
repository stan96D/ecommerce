from django.core.management.base import BaseCommand
from django.db import connection
from ecommerce_website.models import (
    Product, ProductSale, ProductAttributeType, ProductAttribute,
    ProductStock, ProductCategory, ProductFilter, ProductImage
)


class Command(BaseCommand):
    help = 'Delete all data and seed initial data'

    def handle(self, *args, **options):
        # Delete existing data
        models_to_delete = [
            Product, ProductSale, ProductAttributeType, ProductAttribute,
            ProductStock, ProductCategory, ProductFilter, ProductImage
        ]

        for model in models_to_delete:
            model.objects.all().delete()

        # Reset primary key sequences for autoincrement fields
        with connection.cursor() as cursor:
            table_names = [model._meta.db_table for model in models_to_delete]
            for table_name in table_names:
                cursor.execute(
                    f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")

        self.stdout.write(self.style.SUCCESS(
            'All data deleted successfully'))
