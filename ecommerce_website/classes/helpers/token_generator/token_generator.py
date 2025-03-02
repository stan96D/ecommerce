import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from abc import ABC, abstractmethod
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from ecommerce_website.models import *
from django.utils.http import urlsafe_base64_decode
from ecommerce_website.classes.helpers.token_generator.base_token_generator import TokenGeneratorInterface


class ResetPasswordTokenGenerator(TokenGeneratorInterface):

    def __init__(self, user) -> None:
        self.user = user

    def generate(self):
        # Generate a unique token for password reset link (You need to implement this part)
        # Example implementation using Django's token generator

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # Combine uid and token (you may need to format it according to your URL structure)
        reset_token = f"{uid}-{token}"

        return reset_token

    @staticmethod
    def is_token_expired(token):
        try:
            # Split uid and token
            uidb64, token = token.split('-', 1)
            # Decode uid
            uid = urlsafe_base64_decode(uidb64).decode()
            # Get the user object
            user = Account.objects.get(pk=uid)

            # Check if the token is valid and not expired
            return not default_token_generator.check_token(user, token)

        except (ValueError, TypeError, Account.DoesNotExist):
            return True
