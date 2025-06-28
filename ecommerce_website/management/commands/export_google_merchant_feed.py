from datetime import datetime
import os
from django.core.management.base import BaseCommand
from ecommerce_website.services.export_service.google_merchant_export_service import GoogleMerchantExportService


class Command(BaseCommand):
    help = 'Export product data in Google Merchant Center format automatically'

    def handle(self, *args, **options):
        product_export_service = GoogleMerchantExportService()

        # Export data in 'google' format
        export_data = product_export_service.export(file_format='google')

        unique_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        data_folder = os.path.join(
            "ecommerce_website", "reports", "product_export", "google")
        os.makedirs(data_folder, exist_ok=True)

        data_filename = os.path.join(
            data_folder, f"product_export_{unique_id}.xlsx")

        # Write binary data for Excel file
        with open(data_filename, 'wb') as file:
            file.write(export_data)

        self.stdout.write(self.style.SUCCESS(
            f"Exported product data to {data_filename}"))
