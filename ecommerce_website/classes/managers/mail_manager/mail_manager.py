import logging
from email.mime.image import MIMEImage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from abc import ABC, abstractmethod
from ecommerce_website.classes.helpers.token_generator.token_generator import ResetPasswordTokenGenerator
from ecommerce_website.classes.managers.url_manager.url_manager import *
from ecommerce_website.classes.helpers.env_loader import *

url_manager = EncapsulatedURLManager.get_url_manager(EnvLoader.get_env())
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo_url = os.path.join(BASE_DIR,
                        'static', 'images', 'gvs_logo_plain_cropped.jpg')


class BaseMailManager(ABC):

    @abstractmethod
    def send():
        pass


# Set up logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()  # You can also use FileHandler to log to a file
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class HTMLMailManager(BaseMailManager):

    def send(self, sender_email, sender_password, recipient_email, subject, message, timeout=0, image=None):
        try:
            logger.info("Starting email sending process.")
            smtp_server = 'smtp.strato.com'
            smtp_port = 587

            logger.debug(
                f"Connecting to SMTP server: {smtp_server} on port {smtp_port}")
            server = smtplib.SMTP(smtp_server, smtp_port, timeout)
            server.starttls()

            logger.debug(f"Logging in with sender email: {sender_email}")
            server.login(sender_email, sender_password)

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            logger.debug(f"Attaching HTML message content")
            msg.attach(MIMEText(message, 'html'))

            if image:
                logger.debug(f"Attaching image {image}")
                with open(image, 'rb') as img_file:
                    img = MIMEImage(img_file.read(), name="logo.png")
                    img.add_header('Content-ID', '<logo>')
                    msg.attach(img)

            logger.info(f"Sending email to {recipient_email}")
            server.send_message(msg)

            server.quit()

            logger.info("Email sent successfully!")
            return "Email sent successfully!"
        except Exception as e:
            logger.error(f"Failed to send email. Error: {str(e)}")
            return f"Failed to send email. Error: {str(e)}"


class ClientMailSender:

    def __init__(self, mail_manager: BaseMailManager, store_name):
        self.contact_email = os.getenv(
            'ADMIN_EMAIL')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.mail_manager = mail_manager
        self.company_name = store_name
        print("Initializing mail: ", self.sender_email, self.contact_email)

    def send_return_payment_confirmation(self, salutation, last_name, recipient_email, order_number, return_order_url):

        if salutation == "Geen van beiden":
            salutation = "Dhr/Mevr"

        # Add your logo URL here
        subject = "Retournering voor order " + order_number + " betaald!"
        message = f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .email-header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .email-header img {{
                    max-width: 150px;
                    width: 100%;
                    height: auto;
                }}
                .email-content {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333333;
                    margin-bottom: 20px;
                }}
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #f97316; /* Orange color */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #f97316; /* Orange color */
                    color: #ffffff;
                    padding: 10px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                }}
                a.button:hover {{
                    background-color: #FFA000;
                }}
                .service-section {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #fafafa;
                    border-radius: 5px;
                    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
                }}
                .service-header {{
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 15px;
                    font-weight: bold;
                }}
                .service-item {{
                    margin-bottom: 15px;
                }}
                .service-item h4 {{
                    margin: 0;
                    font-size: 16px;
                    color: #333333;
                }}
                .service-item p {{
                    margin: 5px 0 10px 0;
                    color: #555555;
                }}
                a.service-button {{
                    display: inline-block;
                    background-color: #f0f0f0;
                    color: #333333;
                    padding: 8px 16px;
                    border-radius: 5px;
                    margin-top: 10px;
                    text-decoration: none;
                    font-size: 14px;
                }}
                a.service-button:hover {{
                    background-color: #e0e0e0;
                }}
                .image-footer {{
                    text-align: center; /* Center the image */
                    margin-top: 20px;
                }}
                .image-footer img {{
                    max-width: 150px; /* Adjust as needed */
                    width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">

                <div class="email-content">
                    <p>Geachte {salutation} {last_name},</p>
                    <p>Met deze mail willen wij u informeren dat <a href="{return_order_url}">uw betaling</a> in goede handen is ontvangen. Dit betekent dat onze afhaalservice op de hoogte is gebracht van uw retourneringsaanvraag.

                     Zij zullen zo spoedig mogelijk contact met u opnemen. Nadat uw retournering succesvol is opgehaald door onze afhaalservice, duurt het maximaal twee weken totdat uw betaling is teruggestort. Mocht u verder nog vragen hebben neem dan gerust <a href="{url_manager.get_contact_service()}">contact</a> met ons op.
                     Hopelijk heeft u snel uw bestede bedrag terug!</p>
                    <p>Met vriendelijke groet,</p>
                    <p>Het {self.company_name} team</p>
                    <a href="{return_order_url}" class="button">Bekijk uw retournering</a>
                </div>

                <!-- Service & Contact Section -->
                <div class="service-section">
                    <div class="service-header">Service & contact</div>

                    <div class="service-item">
                        <h4>Heb je ons nodig?</h4>
                        <p>Je kunt altijd bij ons terecht met vragen over je retournering.<br>
                        Onze klantenservice is maandag t/m vrijdag van 10:00 tot 17:00 geopend.<br> Mocht er iets met je bestelling aan de hand zijn, dan kun je ons mailen op {self.contact_email} met de vermelding van je bestelnummer.<br>
                        Je bestelnummer voor deze retournering met als order is <strong>{order_number}</strong>.</p>
                        <a href="{url_manager.get_contact_service()}" class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zaken regelen in je account</h4>
                        <p>Volg je order, betaal facturen of retourneer een artikel. Dit kun je allemaal binnen je account doen.</p>
                        <a href="{url_manager.get_account()}" class="service-button">Naar je account</a>
                    </div>
                </div>

                <div class="email-footer">
                    <p>Dit is een automatisch gegenereerde e-mail, antwoorden is niet mogelijk.</p>
                </div>

                <!-- Image Section -->
                <div class="image-footer">
                    <img src="cid:logo" alt="Logo">
                </div>
            </div>
        </body>
        </html>
        """
        return self.mail_manager.send(self.sender_email, self.sender_password,
                                      recipient_email, subject, message, image=logo_url)

    def send_return_confirmation(self, salutation, last_name, recipient_email, order_number, return_order_url):

        if salutation == "Geen van beiden":
            salutation = "Dhr/Mevr"

        # Add your logo URL here
        subject = "Retourneringsbevestiging " + order_number
        message = f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .email-header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .email-header img {{
                    max-width: 150px;
                    width: 100%;
                    height: auto;
                }}
                .email-content {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333333;
                    margin-bottom: 20px;
                }}
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #f97316; /* Orange color */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #f97316; /* Orange color */
                    color: #ffffff;
                    padding: 10px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                }}
                a.button:hover {{
                    background-color: #FFA000;
                }}
                .service-section {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #fafafa;
                    border-radius: 5px;
                    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
                }}
                .service-header {{
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 15px;
                    font-weight: bold;
                }}
                .service-item {{
                    margin-bottom: 15px;
                }}
                .service-item h4 {{
                    margin: 0;
                    font-size: 16px;
                    color: #333333;
                }}
                .service-item p {{
                    margin: 5px 0 10px 0;
                    color: #555555;
                }}
                a.service-button {{
                    display: inline-block;
                    background-color: #f0f0f0;
                    color: #333333;
                    padding: 8px 16px;
                    border-radius: 5px;
                    margin-top: 10px;
                    text-decoration: none;
                    font-size: 14px;
                }}
                a.service-button:hover {{
                    background-color: #e0e0e0;
                }}
                .image-footer {{
                    text-align: center; /* Center the image */
                    margin-top: 20px;
                }}
                .image-footer img {{
                    max-width: 150px; /* Adjust as needed */
                    width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">

                <div class="email-content">
                    <p>Geachte {salutation} {last_name},</p>
                    <p>Bedankt voor uw retourneringsaanvraag!, Hierbij de bevestiging van uw retour voor de order met ordernummer <strong>{order_number}</strong>. De status van je retour order is
                    <a href="{return_order_url}">hier</a> in te zien. Zodra de verzendkosten zijn betaald, wordt uw retournering in behandeling genomen. Wij hopen dit zo spoedig mogelijk voor u te regelen.</p>
                    <p>Met vriendelijke groet,</p>
                    <p>Het {self.company_name} team</p>
                    <a href="{return_order_url}" class="button">Bekijk uw retournering</a>
                </div>

                <!-- Service & Contact Section -->
                <div class="service-section">
                    <div class="service-header">Service & contact</div>

                    <div class="service-item">
                        <h4>Heb je ons nodig?</h4>
                        <p>Je kunt altijd bij ons terecht met vragen over je retournering.<br>
                        Onze klantenservice is maandag t/m vrijdag van 10:00 tot 17:00 geopend.<br> Mocht er iets met je bestelling aan de hand zijn, dan kun je ons mailen op {self.contact_email} met de vermelding van je bestelnummer.<br>
                        Je bestelnummer voor deze retournering met als order is <strong>{order_number}</strong>.</p>
                        <a href="{url_manager.get_contact_service()}" class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zaken regelen in je account</h4>
                        <p>Volg je order, betaal facturen of retourneer een artikel. Dit kun je allemaal binnen je account doen.</p>
                        <a href="{url_manager.get_account()}" class="service-button">Naar je account</a>
                    </div>
                </div>

                <div class="email-footer">
                    <p>Dit is een automatisch gegenereerde e-mail, antwoorden is niet mogelijk.</p>
                </div>

                <!-- Image Section -->
                <div class="image-footer">
                    <img src="cid:logo" alt="Logo">
                </div>
            </div>
        </body>
        </html>
        """
        return self.mail_manager.send(self.sender_email, self.sender_password,
                                      recipient_email, subject, message, image=logo_url)

    def send_order_confirmation(self, salutation, last_name, recipient_email, order_number, order_url):

        if salutation == "Geen van beiden":
            salutation = "Dhr/Mevr"

        # Add your logo URL here
        subject = "Orderbevestiging " + order_number
        message = f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .email-header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .email-header img {{
                    max-width: 150px;
                    width: 100%;
                    height: auto;
                }}
                .email-content {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333333;
                    margin-bottom: 20px;
                }}
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #f97316; /* Orange color */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #f97316; /* Orange color */
                    color: #ffffff;
                    padding: 10px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                }}
                a.button:hover {{
                    background-color: #FFA000;
                }}
                .service-section {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #fafafa;
                    border-radius: 5px;
                    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
                }}
                .service-header {{
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 15px;
                    font-weight: bold;
                }}
                .service-item {{
                    margin-bottom: 15px;
                }}
                .service-item h4 {{
                    margin: 0;
                    font-size: 16px;
                    color: #333333;
                }}
                .service-item p {{
                    margin: 5px 0 10px 0;
                    color: #555555;
                }}
                a.service-button {{
                    display: inline-block;
                    background-color: #f0f0f0;
                    color: #333333;
                    padding: 8px 16px;
                    border-radius: 5px;
                    margin-top: 10px;
                    text-decoration: none;
                    font-size: 14px;
                }}
                a.service-button:hover {{
                    background-color: #e0e0e0;
                }}
                .image-footer {{
                    text-align: center; /* Center the image */
                    margin-top: 20px;
                }}
                .image-footer img {{
                    max-width: 150px; /* Adjust as needed */
                    width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">

                <div class="email-content">
                    <p>Geachte {salutation} {last_name},</p>
                    <p>Bedankt voor uw bestelling!. Hierbij de bevestiging van uw order met ordernummer <strong>{order_number}</strong>. De status van je order is
                    <a href="{order_url}">hier</a> in te zien. Zodra uw bestelling is betaald, wordt uw aankoop in behandeling genomen.
                     We hopen zo spoedig mogelijk je order te verzorgen.</p>
                    <p>Met vriendelijke groet,</p>
                    <p>Het {self.company_name} team</p>
                    <a href="{order_url}" class="button">Bekijk uw bestelling</a>
                </div>

                <!-- Service & Contact Section -->
                <div class="service-section">
                    <div class="service-header">Service & contact</div>

                    <div class="service-item">
                        <h4>Heb je ons nodig?</h4>
                        <p>Je kunt altijd bij ons terecht met vragen over je bestelling.<br>
                        Onze klantenservice is maandag t/m vrijdag van 10:00 tot 17:00 geopend.<br> Mocht er iets met je bestelling aan de hand zijn, dan kun je ons mailen op {self.contact_email} met de vermelding van je bestelnummer.<br>
                        Je bestelnummer voor deze order is <strong>{order_number}</strong>.</p>
                        <a href="{url_manager.get_contact_service()}" class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zaken regelen in je account</h4>
                        <p>Volg je order, betaal facturen of retourneer een artikel. Dit kun je allemaal binnen je account doen.</p>
                        <a href="{url_manager.get_account()}" class="service-button">Naar je account</a>
                    </div>
                </div>

                <div class="email-footer">
                    <p>Dit is een automatisch gegenereerde e-mail, antwoorden is niet mogelijk.</p>
                </div>

                <!-- Image Section -->
                <div class="image-footer">
                    <img src="cid:logo" alt="Logo">
                </div>
            </div>
        </body>
        </html>
        """
        return self.mail_manager.send(self.sender_email, self.sender_password,
                                      recipient_email, subject, message, image=logo_url)

    def send_order_payment_confirmation(self, salutation, last_name, recipient_email, order_number, order_url):

        if salutation == "Geen van beiden":
            salutation = "Dhr/Mevr"

        # Add your logo URL here
        subject = "Order " + order_number + " betaald!"
        message = f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .email-header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .email-header img {{
                    max-width: 150px;
                    width: 100%;
                    height: auto;
                }}
                .email-content {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333333;
                    margin-bottom: 20px;
                }}
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #f97316; /* Orange color */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #f97316; /* Orange color */
                    color: #ffffff;
                    padding: 10px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                }}
                a.button:hover {{
                    background-color: #FFA000;
                }}
                .service-section {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #fafafa;
                    border-radius: 5px;
                    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
                }}
                .service-header {{
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 15px;
                    font-weight: bold;
                }}
                .service-item {{
                    margin-bottom: 15px;
                }}
                .service-item h4 {{
                    margin: 0;
                    font-size: 16px;
                    color: #333333;
                }}
                .service-item p {{
                    margin: 5px 0 10px 0;
                    color: #555555;
                }}
                a.service-button {{
                    display: inline-block;
                    background-color: #f0f0f0;
                    color: #333333;
                    padding: 8px 16px;
                    border-radius: 5px;
                    margin-top: 10px;
                    text-decoration: none;
                    font-size: 14px;
                }}
                a.service-button:hover {{
                    background-color: #e0e0e0;
                }}
                .image-footer {{
                    text-align: center; /* Center the image */
                    margin-top: 20px;
                }}
                .image-footer img {{
                    max-width: 150px; /* Adjust as needed */
                    width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">

                <div class="email-content">
                    <p>Geachte {salutation} {last_name},</p>
                    <p>Met deze mail willen wij u informeren dat <a href="{order_url}">uw betaling</a> in goede handen is ontvangen. Dit betekent dat onze bezorgservice op de hoogte is gebracht van uw bestelling.
                     Zij zullen zo spoedig mogelijk contact met u opnemen. Mocht u verder nog vragen hebben neem dan gerust <a href="{url_manager.get_contact_service()}">contact</a> met ons op.
                     Hopelijk kunt u snel genieten van uw order!</p>
                    <p>Met vriendelijke groet,</p>
                    <p>Het {self.company_name} team</p>
                    <a href="{order_url}" class="button">Bekijk uw bestelling</a>
                </div>

                <!-- Service & Contact Section -->
                <div class="service-section">
                    <div class="service-header">Service & contact</div>

                    <div class="service-item">
                        <h4>Heb je ons nodig?</h4>
                        <p>Je kunt altijd bij ons terecht met vragen over je bestelling.<br>
                        Onze klantenservice is maandag t/m vrijdag van 10:00 tot 17:00 geopend.<br> Mocht er iets met je bestelling aan de hand zijn, dan kun je ons mailen op {self.contact_email} met de vermelding van je bestelnummer.<br>
                        Je bestelnummer voor deze order is <strong>{order_number}</strong>.</p>
                        <a href="{url_manager.get_contact_service()}" class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zaken regelen in je account</h4>
                        <p>Volg je order, betaal facturen of retourneer een artikel. Dit kun je allemaal binnen je account doen.</p>
                        <a href="{url_manager.get_account()}" class="service-button">Naar je account</a>
                    </div>
                </div>

                <div class="email-footer">
                    <p>Dit is een automatisch gegenereerde e-mail, antwoorden is niet mogelijk.</p>
                </div>

                <!-- Image Section -->
                <div class="image-footer">
                    <img src="cid:logo" alt="Logo">
                </div>
            </div>
        </body>
        </html>
        """
        return self.mail_manager.send(self.sender_email, self.sender_password,
                                      recipient_email, subject, message, image=logo_url)

    def send_store_rating(self, salutation, last_name, recipient_email, rating_url):

        if salutation == "Geen van beiden":
            salutation = "Dhr/Mevr"

        # Add your logo URL here

        subject = "Uw mening wordt gevraagd"
        message = f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .email-header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .email-header img {{
                    max-width: 150px;
                }}
                .email-content {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333333;
                    margin-bottom: 20px;
                }}
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #f97316; /* Orange color */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #f97316; /* Orange color */
                    color: #ffffff;
                    padding: 10px 20px;
                    border-radius: 5px;
                    margin-top: 20px;
                    text-decoration: none;
                }}
                a.button:hover {{
                    background-color: #FFA000;
                }}
                .service-section {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #fafafa;
                    border-radius: 5px;
                    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
                }}
                .service-header {{
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 15px;
                    font-weight: bold;
                }}
                .service-item {{
                    margin-bottom: 15px;
                }}
                .service-item h4 {{
                    margin: 0;
                    font-size: 16px;
                    color: #333333;
                }}
                .service-item p {{
                    margin: 5px 0 10px 0;
                    color: #555555;
                }}
                a.service-button {{
                    display: inline-block;
                    background-color: #f0f0f0;
                    color: #333333;
                    padding: 8px 16px;
                    border-radius: 5px;
                    margin-top: 10px;
                    text-decoration: none;
                    font-size: 14px;
                }}
                a.service-button:hover {{
                    background-color: #e0e0e0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">

                <div class="email-content">
                    <p>Geachte {salutation} {last_name},</p>
                    <p>Graag willen wij u vragen of u tijd heeft om uw mening te delen over onze services. Het invullen hiervan duurt slechts één enkele minuut. Dit zal ons op de hoogte houden van de wensen van onze klanten en om deze zo goed mogelijk te verzorgen.</p>
                    <p>U kunt de link <a href="{rating_url}">hier</a> bezoeken. Bedankt voor jullie tijd!</p>
                    <p>Met vriendelijke groet,</p>
                    <p>Het {self.company_name} team</p>
                    <a href="{rating_url}" class="button">Deel uw mening</a>
                </div>

                <!-- Service & Contact Section -->
                <div class="service-section">
                    <div class="service-header">Service & contact</div>

                    <div class="service-item">
                        <h4>Heb je ons nodig?</h4>
                        <p>Je kunt altijd bij ons terecht met vragen over je bestelling of andere gerelateerde zaken.<br> Onze klantenservice is maandag t/m vrijdag van 10:00 tot 17:00 geopend.<br> Mocht er iets met je bestelling aan de hand zijn, dan kun je ons mailen op {self.contact_email}.</p>
                        <a href={url_manager.get_contact_service()} class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zaken regelen in je account</h4>
                        <p>Volg je order, betaal facturen of retourneer een artikel. Dit kun je allemaal binnen je account doen.</p>
                        <a href={url_manager.get_account()} class="service-button">Naar je account</a>
                    </div>
                </div>

                <div class="email-footer">
                    <p>Dit is een automatisch gegenereerde e-mail, antwoorden is niet mogelijk.</p>
                </div>
                <div class="email-header">
                    <img src="cid:logo" alt="Logo">
                </div>
            </div>
        </body>
        </html>
        """
        return self.mail_manager.send(self.sender_email, self.sender_password,
                                      recipient_email, subject, message, image=logo_url)


class AdminMailSender:

    def __init__(self, mail_manager: BaseMailManager, store_name):
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_email = os.getenv('ADMIN_EMAIL')
        self.mail_manager = mail_manager
        self.company_name = store_name

    def send_order_confirmation(self, order):
        subject = f"Orderbevestiging {order.order_number} {
            order.first_name} {order.last_name}"

        # Group order lines by supplier
        supplier_order_lines = {}
        for line in order.order_lines.all():
            supplier = line.product.supplier
            if supplier not in supplier_order_lines:
                supplier_order_lines[supplier] = []
            supplier_order_lines[supplier].append(line)

        # Generate the order lines sections for each supplier
        order_lines_sections = ""
        for supplier, lines in supplier_order_lines.items():
            supplier_lines_text = ""
            for line in lines:
                supplier_lines_text += f"<li>{line.product.name} (Aantal: {
                    line.quantity}, Totaalprijs: €{line.total_price})</li>"

            order_lines_sections += f"""
            <div class="order-details">
                <h3>Leverancier: {supplier}</h3>
                <ul>
                    {supplier_lines_text}
                </ul>
            </div>
            <hr>
            """

        message = f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    font-size: 18px;
                    margin-bottom: 20px;
                }}
                .header p {{
                    margin: 5px 0;
                }}
                .email-content {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333333;
                }}
                .email-content p {{
                    margin: 5px 0;
                }}
                .email-content .address-block {{
                    margin-top: 15px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    border: 1px solid #dddddd;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }}
                .email-content .address-block p {{
                    margin: 5px 0;
                }}
                .order-details {{
                    margin-top: 20px;
                }}
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #f97316; /* Orange kleur */
                    text-decoration: none;
                }}
                ul {{
                    padding-left: 20px;
                    margin: 10px 0;
                }}
                li {{
                    margin-bottom: 10px;
                }}
                hr {{
                    border: 0;
                    border-top: 1px solid #dddddd;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <p>Hallo,</p>
                    <p>Hierbij de orderbevestiging met ordernummer <strong>{order.order_number}</strong> voor <strong>{order.first_name} {order.last_name}</strong>.</p>
                </div>
                <div class="email-content">
                    <p><strong>Email:</strong> {order.email}</p>
                    <p><strong>Telefoonnummer:</strong> {order.phone}</p>

                    <div class="address-block">
                        <p><strong>Adres:</strong></p>
                        <p>{order.shipping_address} </p>
                    </div>

                    {order_lines_sections}

                    <p><strong>Gewenste leverdatum:</strong> {order.deliver_date}</p>

                </div>
                <div class="email-footer">
                    <p>Met vriendelijke groet,</p>
                    <p>Het {self.company_name} team!</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.mail_manager.send(self.sender_email, self.sender_password,
                                      self.recipient_email, subject, message)

    def send_return_order_confirmation(self, return_order):
        subject = f"Retourbevestiging {return_order.order.order_number} {
            return_order.order.first_name} {return_order.order.last_name}"

        full_address = "{}&nbsp;{} \n{}&nbsp;{} \n{}".format(
            return_order.address, return_order.house_number, return_order.postal_code, return_order.city, return_order.country)

        # Group order lines by supplier
        supplier_order_lines = {}
        for line in return_order.return_order_lines.all():
            supplier = line.order_line.product.supplier
            if supplier not in supplier_order_lines:
                supplier_order_lines[supplier] = []
            supplier_order_lines[supplier].append(line)

        # Generate the order lines sections for each supplier
        order_lines_sections = ""
        for supplier, lines in supplier_order_lines.items():
            supplier_lines_text = ""
            for line in lines:
                supplier_lines_text += f"<li>{line.order_line.product.name} (Aantal: {
                    line.quantity}, Totaalprijs: €{line.refund_amount})</li>"

            order_lines_sections += f"""
            <div class="order-details">
                <h3>Leverancier: {supplier}</h3>
                <ul>
                    {supplier_lines_text}
                </ul>
            </div>
            <hr>
            """

        message = f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    font-size: 18px;
                    margin-bottom: 20px;
                }}
                .header p {{
                    margin: 5px 0;
                }}
                .email-content {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333333;
                }}
                .email-content p {{
                    margin: 5px 0;
                }}
                .email-content .address-block {{
                    margin-top: 15px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    border: 1px solid #dddddd;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }}
                .email-content .address-block p {{
                    margin: 5px 0;
                }}
                .order-details {{
                    margin-top: 20px;
                }}
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #f97316; /* Orange kleur */
                    text-decoration: none;
                }}
                ul {{
                    padding-left: 20px;
                    margin: 10px 0;
                }}
                li {{
                    margin-bottom: 10px;
                }}
                hr {{
                    border: 0;
                    border-top: 1px solid #dddddd;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <p>Hallo,</p>
                    <p>Hierbij de retourbevestiging met ordernummer <strong>{return_order.id}/{return_order.order.order_number}</strong> voor <strong>{return_order.first_name} {return_order.last_name}</strong>.</p>
                </div>
                <div class="email-content">
                    <p><strong>Email:</strong> {return_order.email_address}</p>
                    <p><strong>Telefoonnummer:</strong> {return_order.phone}</p>

                    <div class="address-block">
                        <p><strong>Adres:</strong></p>
                        <p>{full_address} </p>
                    </div>

                    {order_lines_sections}

                    <p><strong>Gewenste leverdatum:</strong> {return_order.deliver_date}</p>

                </div>
                <div class="email-footer">
                    <p>Met vriendelijke groet,</p>
                    <p>Het {self.company_name} team!</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.mail_manager.send(self.sender_email, self.sender_password,
                                      self.recipient_email, subject, message)


class ForgotPasswordMailSender:

    def __init__(self, mail_manager: BaseMailManager, store_name):
        self.contact_email = os.getenv('ADMIN_EMAIL')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.mail_manager = mail_manager
        self.company_name = store_name

    def send_password_reset_email(self, user):
        # Generate the reset password URL with token
        token_generator = ResetPasswordTokenGenerator(user)
        token = token_generator.generate()
        reset_password_confirm_url = f"http://127.0.0.1:8000/new_password/{
            token}/"

        subject = "Aanvraag wachtwoord resetten"
        message = f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .email-header {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 20px;
                }}
                .email-header img {{
                    max-width: 200px; /* Adjust as needed */
                    width: 100%;
                    height: auto;
                }}
                .email-content {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333333;
                    margin-bottom: 20px;
                }}
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #f97316; /* Orange kleur */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #f97316; /* Orange kleur */
                    color: #ffffff;
                    padding: 10px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                }}
                a.button:hover {{
                    background-color: #FFA000;
                }}
                .service-section {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #fafafa;
                    border-radius: 5px;
                    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
                }}
                .service-header {{
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 15px;
                    font-weight: bold;
                }}
                .service-item {{
                    margin-bottom: 15px;
                }}
                .service-item h4 {{
                    margin: 0;
                    font-size: 16px;
                    color: #333333;
                }}
                .service-item p {{
                    margin: 5px 0 10px 0;
                    color: #555555;
                }}
                a.service-button {{
                    display: inline-block;
                    background-color: #f0f0f0;
                    color: #333333;
                    padding: 8px 16px;
                    border-radius: 5px;
                    margin-top: 10px;
                    text-decoration: none;
                    font-size: 14px;
                }}
                a.service-button:hover {{
                    background-color: #e0e0e0;
                }}
                .image-footer {{
                    text-align: center; /* Center the image */
                    margin-top: 20px;
                }}
                .image-footer img {{
                    max-width: 150px; /* Adjust as needed */
                    width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">

                <div class="email-content">
                    <p>Beste {user.first_name},</p>
                    <p>We hebben een verzoek ontvangen om je wachtwoord te resetten. Deze kun je <a href="{reset_password_confirm_url}">hier</a> aanpassen</p>
                    <p>Als je dit wachtwoord reset verzoek niet hebt aangevraagd, negeer dan deze e-mail.</p>
                                        <a href="{reset_password_confirm_url}" class="button">Wachtwoord resetten</a>

                    <p>Met vriendelijke groet,</p>
                    <p>Het {self.company_name} team</p>
                </div>

                <!-- Service & Contact Section -->
                <div class="service-section">
                    <div class="service-header">Service & Contact</div>

                    <div class="service-item">
                        <h4>Heb je ons nodig?</h4>
                        <p>Je kunt altijd bij ons terecht met vragen over je account of andere zaken.<br> Onze klantenservice is bereikbaar via e-mail op {self.contact_email}.<br> We zijn bereikbaar maandag tot vrijdag van 10:00 tot 17:00.</p>
                        <a href="{url_manager.get_contact_service()}" class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zelf regelen</h4>
                        <p>Volg je bestelling, betaal facturen of retourneer artikelen door in te loggen op je account. Allemaal eenvoudig geregeld binnen je account.</p>
                        <a href="{url_manager.get_account()}" class="service-button">Naar je account</a>
                    </div>
                </div>

                <div class="email-footer">
                    <p>Dit is een automatisch gegenereerde e-mail, antwoorden is niet mogelijk.</p>
                </div>

                <!-- Image Section -->
                <div class="image-footer">
                    <img src="cid:logo" alt="Logo">
                </div>
            </div>
        </body>
        </html>
        """

        return self.mail_manager.send(
            self.sender_email, self.sender_password, user.email, subject, message, image=logo_url
        )
