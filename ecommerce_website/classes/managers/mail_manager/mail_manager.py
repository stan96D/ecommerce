import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class MailManager:


    def send(self, sender_email, sender_password, recipient_email, subject, message):
        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            server.login(sender_email, sender_password)

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'html'))

            server.send_message(msg)

            server.quit()

            return "Email sent successfully!"
        except Exception as e:
            return f"Failed to send email. Error: {str(e)}"


class ClientMailSender():

    text = "Geachte {salutation} {last_name},\n\n Hierbij de bevestiging van uw order met ordernummer {order_number}. De status van je order is <a href='{order_url}'>hier</a> in te zien. We hopen zo snel mogelijk je order te verzorgen.\n\nMet vriendelijke groet,\n\nHet goedkopevloeren.nl team!"

    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.mail_manager = MailManager()

    def send_order_confirmation(self, salutation, last_name, recipient_email, order_number, order_url):

        subject = "Orderbevestiging " + order_number

        message = self.text.format(
            salutation=salutation, last_name=last_name, order_number=order_number, order_url=order_url)
        
        return self.mail_manager.send(self.sender_email, self.sender_password,
                  recipient_email, subject, message)


class AdminMailSender():


    text = """Hallo,

    Hierbij de orderbevestiging met ordernummer {order_number} voor persoon {first_name} {last_name}.

    Orderlines:
    {order_lines}

    Met vriendelijke groet,

    Het goedkopevloeren.nl team!
    """

    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_email = os.getenv('ADMIN_EMAIL')
        self.mail_manager = MailManager()

    def send_order_confirmation(self, first_name, last_name, order_number, order_lines):

        subject = "Orderbevestiging " + order_number + " " + first_name + " " + last_name


        order_lines_text = ""
        for line in order_lines.all():
            order_lines_text += f"{line.product.name
                                } (Aantal: {line.quantity}, Totaalprijs: ${line.total_price})\n"

        message = self.text.format(
            first_name=first_name,
            last_name=last_name,
            order_number=order_number,
            order_lines=order_lines_text
)

        # message = self.text.format(
        #     first_name=first_name, last_name=last_name, order_number=order_number)

        return self.mail_manager.send(self.sender_email, self.sender_password,
                               self.recipient_email, subject, message)
