from email.mime.image import MIMEImage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from abc import ABC, abstractmethod
from ecommerce_website.classes.helpers.token_generator.token_generator import ResetPasswordTokenGenerator
from ecommerce_website.classes.managers.url_manager.url_manager import *


class BaseMailManager(ABC):

    @abstractmethod
    def send():
        pass


class HTMLMailManager(BaseMailManager):

    def send(self, sender_email, sender_password, recipient_email, subject, message, timeout=0, image=None):
        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            server = smtplib.SMTP(smtp_server, smtp_port, timeout)
            server.starttls()

            server.login(sender_email, sender_password)

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'html'))

            if image:

                with open(image, 'rb') as img_file:
                    img = MIMEImage(img_file.read(), name="logo.png")
                    img.add_header('Content-ID', '<logo>')
                    msg.attach(img)

            server.send_message(msg)

            server.quit()

            return "Email sent successfully!"
        except Exception as e:
            return f"Failed to send email. Error: {str(e)}"


class ClientMailSender:

    def __init__(self, mail_manager: BaseMailManager):
        self.contact_email = os.getenv(
            'SENDER_EMAIL')  # TODO set to contact mail
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.mail_manager = mail_manager

    def send_order_confirmation(self, salutation, last_name, recipient_email, order_number, order_url):
        # Add your logo URL here
        logo_url = "ecommerce_website/static/images/gvs_logo_text.png"
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
                    color: #FFB300; /* Amber color */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #FFB300; /* Amber color */
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
                    <p>Hierbij de bevestiging van uw order met ordernummer <strong>{order_number}</strong>. De status van je order is
                    <a href="{order_url}">hier</a> in te zien. We hopen zo snel mogelijk je order te verzorgen.</p>
                    <p>Met vriendelijke groet,</p>
                    <p>Het goedkopevloeren.nl team</p>
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
                        <a href="{TestURLManager.get_contact_service()}" class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zaken regelen in je account</h4>
                        <p>Volg je order, betaal facturen of retourneer een artikel. Dit kun je allemaal binnen je account doen.</p>
                        <a href="{TestURLManager.get_account()}" class="service-button">Naar je account</a>
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
        # Add your logo URL here
        logo_url = "ecommerce_website/static/images/gvs_logo_text.png"

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
                    color: #FFB300; /* Amber color */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #FFB300; /* Amber color */
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
                    <p>Het goedkopevloeren.nl team</p>
                    <a href="{rating_url}" class="button">Deel uw mening</a>
                </div>

                <!-- Service & Contact Section -->
                <div class="service-section">
                    <div class="service-header">Service & contact</div>

                    <div class="service-item">
                        <h4>Heb je ons nodig?</h4>
                        <p>Je kunt altijd bij ons terecht met vragen over je bestelling of andere gerelateerde zaken.<br> Onze klantenservice is maandag t/m vrijdag van 10:00 tot 17:00 geopend.<br> Mocht er iets met je bestelling aan de hand zijn, dan kun je ons mailen op {self.contact_email}.</p>
                        <a href={TestURLManager.get_contact_service()} class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zaken regelen in je account</h4>
                        <p>Volg je order, betaal facturen of retourneer een artikel. Dit kun je allemaal binnen je account doen.</p>
                        <a href={TestURLManager.get_account()} class="service-button">Naar je account</a>
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

    def __init__(self, mail_manager: BaseMailManager):
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_email = os.getenv('ADMIN_EMAIL')
        self.mail_manager = mail_manager

    def send_order_confirmation(self, order):

        subject = f"Orderbevestiging {order.order_number} {
            order.first_name} {order.last_name}"

        order_lines_text = ""
        for line in order.order_lines.all():
            order_lines_text += f"<li>{line.product.name} (Aantal: {
                line.quantity}, Totaalprijs: €{line.total_price})</li>"

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
                .email-footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777777;
                    text-align: center;
                }}
                a {{
                    color: #FFB300; /* Amber kleur */
                    text-decoration: none;
                }}
                ul {{
                    padding-left: 20px;
                    margin: 10px 0;
                }}
                li {{
                    margin-bottom: 10px;
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
                    <p><strong>Email:</strong> {order.account.email}</p>
                    <p><strong>Telefoonnummer:</strong> {order.account.phone_number}</p>

                    <div class="address-block">
                        <p><strong>Adres:</strong></p>
                        <p>{order.account.address} {order.account.house_number}</p>
                        <p>{order.account.city}, {order.account.postal_code}</p>
                        <p>{order.account.country}</p>
                    </div>

                    <div class="order-details">
                        <p><strong>Orderregels:</strong></p>
                        <ul>
                            {order_lines_text}
                        </ul>
                    </div>
                </div>
                <div class="email-footer">
                    <p>Met vriendelijke groet,</p>
                    <p>Het goedkopevloeren.nl team!</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.mail_manager.send(self.sender_email, self.sender_password,
                                      self.recipient_email, subject, message)


class ForgotPasswordMailSender:

    def __init__(self, mail_manager: BaseMailManager):
        self.contact_email = os.getenv('SENDER_EMAIL')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.mail_manager = mail_manager

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
                    color: #FFB300; /* Amber kleur */
                    text-decoration: none;
                }}
                a.button {{
                    display: inline-block;
                    background-color: #FFB300; /* Amber kleur */
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
                    <p>Het goedkopevloeren.nl team</p>
                </div>

                <!-- Service & Contact Section -->
                <div class="service-section">
                    <div class="service-header">Service & Contact</div>

                    <div class="service-item">
                        <h4>Heb je ons nodig?</h4>
                        <p>Je kunt altijd bij ons terecht met vragen over je account of andere zaken.<br> Onze klantenservice is bereikbaar via e-mail op {self.contact_email}.<br> We zijn bereikbaar maandag tot vrijdag van 10:00 tot 17:00.</p>
                        <a href="{TestURLManager.get_contact_service()}" class="service-button">Naar de klantenservicepagina</a>
                    </div>

                    <div class="service-item">
                        <h4>Zelf regelen</h4>
                        <p>Volg je bestelling, betaal facturen of retourneer artikelen door in te loggen op je account. Allemaal eenvoudig geregeld binnen je account.</p>
                        <a href="{TestURLManager.get_account()}" class="service-button">Naar je account</a>
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

        logo_url = "ecommerce_website/static/images/gvs_logo_text.png"

        return self.mail_manager.send(
            self.sender_email, self.sender_password, user.email, subject, message, image=logo_url
        )
