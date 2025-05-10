import os
import json
import traceback
from django.core.management.base import BaseCommand
from ecommerce_website.seeders.product_updater import ProductUpdater
from ecommerce_website.classes.managers.mail_manager.mail_manager import HTMLMailManager


class Command(BaseCommand):
    help = 'Update product data into the database and enlight the board'

    def handle(self, *args, **options):
        try:
            # Load the product data from the JSON file
            with open('ecommerce_website/seeders/updated_product_data/product_data.json', 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            # Update products and get the file path
            updater = ProductUpdater()
            file_name = updater.update_products(json_data)

            self.stdout.write(self.style.SUCCESS(
                'Updated product data successfully added'))

            # Now parse the report file to get SKUs to deactivate
            try:
                with open(file_name, 'r', encoding='utf-8') as report_file:
                    report_data = json.load(report_file)

                not_updated_skus = report_data.get(
                    "products", {}).get("not_updated", [])
                if not_updated_skus:
                    deactivated_count = updater.deactivate_products_by_skus(
                        not_updated_skus)
                    self.stdout.write(self.style.WARNING(
                        f"{deactivated_count} products were deactivated."))
                else:
                    self.stdout.write(self.style.NOTICE(
                        "No products to deactivate."))

            except Exception as e:
                self.stderr.write(self.style.ERROR(
                    f"Failed to read report file or deactivate products: {e}"))
                traceback.print_exc()

            # Now, let's send the email with the attached report file
            self.send_email_with_attachment(file_name)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
            traceback.print_exc()
            self.stdout.write(self.style.WARNING(
                'An error occurred. Running cleanup command...'))

    def send_email_with_attachment(self, file_path):
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        recipient_email = 'stan-deckers@live.nl'
        subject = 'Product Data Update Rapportage'

        message = (
            "Hallo,<br><br>"
            "In de bijlage vindt u het rapport met de bijgewerkte productgegevens.<br><br>"
            "Met vriendelijke groet,<br>"
            "<strong>Het team van Goedkoopstevloerenshop.nl</strong>"
        )

        mail_manager = HTMLMailManager()
        result = mail_manager.send_file(
            sender_email=sender_email,
            sender_password=sender_password,
            recipient_email=recipient_email,
            subject=subject,
            message=message,
            file=file_path
        )

        if "Email sent successfully" in result:
            self.stdout.write(self.style.SUCCESS(
                f'Email sent successfully with report attached: {file_path}'))
        else:
            self.stderr.write(self.style.ERROR(
                f"Failed to send email: {result}"))
