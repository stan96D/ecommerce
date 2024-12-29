# core/management/commands/send_html_test_email.py

from django.core.management.base import BaseCommand
# Import your custom HTMLMailManager
from ecommerce_website.classes.managers.mail_manager.mail_manager import ClientMailSender, HTMLMailManager
import os  # Import os for environment variables


class Command(BaseCommand):
    help = 'Sends a test HTML email using the HTMLMailManager'

    def handle(self, *args, **kwargs):
        # Define the email parameters
        # Replace with the actual recipient email
        recipient_email = 'stan-deckers@live.nl'

        # Fetch email credentials from environment variables
        # Environment variable for the sender email
        sender_email = os.getenv('SENDER_EMAIL')
        # Environment variable for the sender password
        sender_password = os.getenv('SENDER_PASSWORD')

        if not sender_email or not sender_password:
            self.stdout.write(self.style.ERROR(
                'Error: Email credentials not found in environment variables.'))
            return

        result = ClientMailSender(mail_manager=HTMLMailManager(), store_name="goedkopevloerenshop.nl").send_order_confirmation("Hoi",
                                                                                                                               "Test",
                                                                                                                               recipient_email,
                                                                                                                               "testorder",
                                                                                                                               "not_working")

        # Print the result
        self.stdout.write(self.style.SUCCESS(result))
