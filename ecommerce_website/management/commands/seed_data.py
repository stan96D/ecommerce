from django.core.management.base import BaseCommand
from ecommerce_website.seeders.product_seeder import ProductSeeder, ProductAttributeTypeSeeder, ProductAttributeSeeder


class Command(BaseCommand):
    help = 'Seed initial data into the database'

    def handle(self, *args, **options):
        ProductSeeder.seed()
        ProductAttributeTypeSeeder.seed()
        ProductAttributeSeeder.seed()

        self.stdout.write(self.style.SUCCESS('Seed data successfully added'))
