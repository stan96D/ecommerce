from django.core.management.base import BaseCommand
from django.db import connection
from ecommerce_website.seeders.real_seeder import *
from ecommerce_website.models import *


class Command(BaseCommand):
    help = 'Seed more product data into the database'

    def handle(self, *args, **options):

        RealProductDataSeeder.add(
            'ecommerce_website/db_mapper/data/manual_products.json')
        # RealProductFilterSeeder.seed()

        self.stdout.write(self.style.SUCCESS('Seed data successfully added'))
