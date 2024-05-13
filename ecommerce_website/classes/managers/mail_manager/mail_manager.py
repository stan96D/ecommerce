import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailManager:

    def send(sender_email, sender_password, recipient_email, subject, message):

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server.send_message(msg)

        server.quit()


class ClientMailSender():

    text = "Geachte {salutation} {last_name},\n\n Hierbij de bevestiging van uw order met ordernummer {order_id}. De status van je order is <a href='{order_url}'>hier</a> in te zien. We hopen zo snel mogelijk je order te verzorgen.\n\nMet vriendelijke groet,\n\nHet goedkopevloeren.nl team!"

    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.mail_manager = MailManager()


    def send_order_confirmation(self, salutation, last_name, recipient_email, order_id, order_url):

        subject = "Orderbevestiging " + order_id
        
        message = self.text.format(
            salutation=salutation, last_name=last_name, order_id=order_id, order_url=order_url)
        
        self.mail_manager.send(self.sender_email, self.sender_password,
                  recipient_email, subject, message)
