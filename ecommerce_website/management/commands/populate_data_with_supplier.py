from django.core.management.base import BaseCommand
from django.db import connection
from ecommerce_website.classes.helpers.add_missing_value_to_list_of_objects import *
from django.conf import settings


class Command(BaseCommand):
    help = 'Populate the json file with missing property and values'

    def handle(self, *args, **options):

        shared_property = "Leverancier"


        peitsman_data_file = r'ecommerce_website\db_mapper\data\finalized_data2.json'
        peitsman_data = "Peitsman"

        modify_json_file(peitsman_data_file, shared_property, peitsman_data)

        ppc_data_file = "ecommerce_website\db_mapper\data\ppc_finalized.json"
        ppc_data = "PPC"

        modify_json_file(ppc_data_file, shared_property, ppc_data)
