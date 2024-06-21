from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from abc import ABC, abstractmethod
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from ecommerce_website.models import *
from django.utils.http import urlsafe_base64_decode


class TokenGeneratorInterface(ABC):

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def is_token_expired(token):
        pass
