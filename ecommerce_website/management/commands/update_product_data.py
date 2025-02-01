from django.core.management.base import BaseCommand
from django.core.management import call_command
from ecommerce_website.seeders.product_updater import ProductUpdater
from ecommerce_website.seeders.production_seeder import ProductionSeeder
import json
import traceback


class Command(BaseCommand):
    help = 'Update product data into the database'

    def handle(self, *args, **options):
        try:
            with open('ecommerce_website/seeders/updated_product_data/product_data.json', 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            ProductUpdater().update_products(json_data)

            self.stdout.write(self.style.SUCCESS(
                'Updated product data successfully added'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
            traceback.print_exc()

            # Call the cleanup command
            self.stdout.write(self.style.WARNING(
                'An error occurred. Running cleanup command...'))
