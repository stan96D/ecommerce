import inquirer
from datetime import datetime
import os
from django.core.management.base import BaseCommand
from ecommerce_website.services.export_service.product_export_service import ProductExportService


class Command(BaseCommand):
    help = 'Export product data from the database'

    def handle(self, *args, **options):
        # Ask user to select the export format interactively
        questions = [
            inquirer.List(
                'format',
                message="Select the export format",
                choices=['csv', 'json', 'excel'],
                default='csv',  # Default is CSV
            ),
        ]
        answers = inquirer.prompt(questions)
        file_format = answers['format']

        # For Products
        product_export_service = ProductExportService()
        export_data = product_export_service.export(file_format=file_format)

        # Generate a unique timestamp for the filename
        unique_id = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS

        # Define the base folder and file path for the report
        data_folder = os.path.join(
            "ecommerce_website", "reports", "product_export", file_format)
        os.makedirs(data_folder, exist_ok=True)  # Ensure the directory exists

        # Define the full file path with the timestamped filename
        if file_format == 'csv':
            data_filename = os.path.join(
                data_folder, f"product_export_{unique_id}.csv")
        elif file_format == 'json':
            data_filename = os.path.join(
                data_folder, f"product_export_{unique_id}.json")
        elif file_format == 'excel':
            data_filename = os.path.join(
                data_folder, f"product_export_{unique_id}.xlsx")

        # Save the exported data to a file
        if file_format == 'csv':
            with open(data_filename, 'w', encoding='utf-8-sig') as file:
                file.write(export_data)
        elif file_format == 'json':
            with open(data_filename, 'w', encoding='utf-8') as file:
                file.write(export_data)
        elif file_format == 'excel':
            with open(data_filename, 'wb') as file:  # Binary write for Excel
                file.write(export_data)

        self.stdout.write(self.style.SUCCESS(
            f"Exported product data to {data_filename}"))
