from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ecommerce_website.models import Account


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("De wachtwoorden komen niet overeen."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].error_messages['required'] = _(
            'Dit veld is vereist.')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # Handle all password validation errors manually for password1
        try:
            # Validate password using Django's default password validators
            validate_password(
                password, self.instance, password_validators=get_default_password_validators())
        except ValidationError as e:
            # Translate any validation errors to Dutch here
            error_translations = {
                "This password is too short. It must contain at least 8 characters.":
                    "Het wachtwoord moet minimaal 8 tekens lang zijn.",
                "This password is too common.":
                    "Dit wachtwoord is te algemeen, kies een sterker wachtwoord.",
                "This password is entirely numeric.":
                    "Het wachtwoord mag niet alleen uit cijfers bestaan.",
                "The password is too similar to the email address.":
                    "Het wachtwoord lijkt te veel op het e-mailadres.",
                "The password is too similar to your other personal information.":
                    "Het wachtwoord lijkt te veel op uw persoonlijke gegevens."
            }

            # Replace default error messages with translated ones
            translated_errors = [error_translations.get(
                msg, _("Wachtwoordfout: ") + msg) for msg in e.messages]
            raise ValidationError(translated_errors)

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Check if the passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'])

        # Handle all password validation errors manually for password2
        try:
            # Validate password using Django's default password validators (for password2)
            validate_password(password2, self.instance,
                              password_validators=get_default_password_validators())
        except ValidationError as e:
            # Translate any validation errors to Dutch here for password2
            error_translations = {
                "This password is too short. It must contain at least 8 characters.":
                    "Het wachtwoord moet minimaal 8 tekens lang zijn.",
                "This password is too common.":
                    "Dit wachtwoord is te algemeen, kies een sterker wachtwoord.",
                "This password is entirely numeric.":
                    "Het wachtwoord mag niet alleen uit cijfers bestaan.",
                "The password is too similar to the email address.":
                    "Het wachtwoord lijkt te veel op het e-mailadres.",
                "The password is too similar to your other personal information.":
                    "Het wachtwoord lijkt te veel op uw persoonlijke gegevens."
            }

            # Replace default error messages with translated ones for password2
            translated_errors = [error_translations.get(
                msg, _("Wachtwoordfout: ") + msg) for msg in e.messages]
            raise ValidationError(translated_errors)

        return password2

    class Meta:
        model = Account
        fields = ['email', 'password1', 'first_name', 'last_name', 'phone_number',
                  'salutation', 'postal_code', 'address', 'house_number', 'country', 'city']

        error_messages = {field: {'required': _(
            'Dit veld is vereist.')} for field in fields}

        error_messages['email'] = {
            'unique': _('Dit e-mailadres kan niet gebruikt worden.')
        }
