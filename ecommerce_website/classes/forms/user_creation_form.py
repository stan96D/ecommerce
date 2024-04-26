from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ecommerce_website.models import Account
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):

    error_messages = {
        'password_mismatch': _("De wachtwoorden komen niet overeen.")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password2'].error_messages['required'] = _(
            'Dit veld is vereist.')
        

    class Meta:
        model = Account
        fields = ['email', 'password1', 'first_name', 'last_name', 'phone_number',
                  'salutation', 'postal_code', 'address', 'house_number', 'country', 'city']

        error_messages = {}
        for field_name in fields:
            error_messages[field_name] = {
                'required': _('Dit veld is vereist.')
            }

        error_messages['email'] = {
            'unique': _('Dit e-mailadres kan niet gebruikt worden.')
        }


