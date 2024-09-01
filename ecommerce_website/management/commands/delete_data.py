from django.core.management.base import BaseCommand
from django.db import connection
import os
from django.conf import settings
from ecommerce_website.models import (
    Product, ProductSale, Sale, ProductAttributeType, ProductAttribute,
    ProductStock, ProductCategory, ProductFilter, Order, OrderLine,
    DeliveryMethod, StoreMotivation, StoreRating, Brand, ReturnOrderLine, ReturnOrder
)


class Command(BaseCommand):
    help = 'Delete all data and seed initial data'

    def handle(self, *args, **options):
        # Delete existing data
        models_to_delete = [
            Product, ProductSale, Sale, ProductAttributeType, ProductAttribute,
            ProductStock, ProductCategory, ProductFilter, Order, OrderLine,
            DeliveryMethod, StoreMotivation, StoreRating, Brand, ReturnOrderLine, ReturnOrder
        ]

        for model in models_to_delete:
            model.objects.all().delete()

        # Reset primary key sequences for autoincrement fields
        with connection.cursor() as cursor:
            table_names = [model._meta.db_table for model in models_to_delete]
            for table_name in table_names:
                cursor.execute(
                    f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")

        # Delete product thumbnails
        media_directory = os.path.join(
            settings.MEDIA_ROOT, 'product_thumbnails')
        if os.path.isdir(media_directory):
            for filename in os.listdir(media_directory):
                file_path = os.path.join(media_directory, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    self.stderr.write(f"Failed to delete {
                                      file_path}. Reason: {e}")


        self.stdout.write(self.style.SUCCESS(
            'All data deleted successfully'))
