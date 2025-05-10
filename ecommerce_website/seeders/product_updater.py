import os
import json
from datetime import datetime
from decimal import Decimal
from ecommerce_website.services.database_import_service.product_update_service import ProductUpdateService
from ecommerce_website.models import Product
from django.db import transaction


class ProductUpdater:
    def deactivate_products_by_skus(self, sku_list):
        """
        Bulk deactivate products by setting 'active' to False based on a list of SKUs.
        """
        if not sku_list:
            print("No SKUs provided to deactivate.")
            return 0

        try:
            with transaction.atomic():
                updated_count = Product.objects.filter(
                    sku__in=sku_list).update(active=False)
                print(f"{updated_count} products deactivated.")
                return updated_count
        except Exception as e:
            print(f"Failed to deactivate products: {str(e)}")
            return 0

    def update_products(self, products_data_json):
        # Generate the report by importing product data
        reports = ProductUpdateService().import_product_data(products_data_json)

        # Generate a unique timestamp for the filename
        unique_id = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS

        # Define the folder and file path for the report
        data_folder = os.path.join(
            "ecommerce_website/reports", "update_data_report")
        os.makedirs(data_folder, exist_ok=True)  # Ensure the directory exists

        # Define the full file path with the timestamped filename
        data_filename = os.path.join(
            data_folder, f"products_updated_{unique_id}.json")

        # Ensure the report is serializable by handling non-JSON types
        def serialize_special(obj):
            if isinstance(obj, Decimal):
                # or float(obj) if numeric representation is desired
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")

        # Write the report to the file
        try:
            with open(data_filename, "w", encoding="utf-8") as report_file:
                json.dump(reports, report_file, indent=4,
                          ensure_ascii=False, default=serialize_special)
            print(f"Report successfully written to {data_filename}")
        except Exception as e:
            print(f"Failed to write report: {str(e)}")

        return data_filename  # Return the path to the generated report
