from django.core.management.base import BaseCommand
from django.core.management import call_command
from ecommerce_website.seeders.production_seeder import ProductionSeeder
import json
import traceback


class Command(BaseCommand):
    help = 'Seed initial data into the database'

    def handle(self, *args, **options):
        try:
            with open('ecommerce_website/seeders/dynamic_seeder_data/product_data.json', 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            ProductionSeeder().seed_initial(json_data)

            self.stdout.write(self.style.SUCCESS(
                'Seed data successfully added'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
            traceback.print_exc()

            # Call the cleanup command
            self.stdout.write(self.style.WARNING(
                'An error occurred. Running cleanup command...'))
            try:
                # Replace with the name of your cleanup command
                call_command('delete_data')
                self.stdout.write(self.style.SUCCESS(
                    'Cleanup command executed successfully.'))
            except Exception as cleanup_error:
                self.stderr.write(self.style.ERROR(
                    f"Error while running cleanup command: {cleanup_error}"))
                traceback.print_exc()
