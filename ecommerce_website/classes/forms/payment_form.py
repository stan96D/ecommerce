from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class PaymentForm(forms.Form):
    issuer_id = forms.CharField(required=False)
    issuer_name = forms.CharField(required=False)
    payment_method = forms.CharField(
        required=True,
        error_messages={'required': 'Selecteer een betaalmethode.'}
    )
    payment_name = forms.CharField(required=True)
    selected_delivery_method = forms.CharField(
        required=True,
        error_messages={'required': 'Selecteer een verzendmethode.'}
    )
    delivery_date = forms.CharField(
        required=True,
        error_messages={'required': 'Kies een bezorgdatum.'},
        widget=forms.DateInput(format='%d-%m-%Y')  # Custom format
    )

    def clean_delivery_date(self):
        # Getting the raw string input from the form
        delivery_date_str = self.cleaned_data.get('delivery_date')

        # Parse the custom date format (dd-mm-yyyy) to a datetime object
        try:
            delivery_date = datetime.strptime(
                delivery_date_str, '%d-%m-%Y').date()
        except ValueError:
            raise ValidationError('Ongeldig datumformaat, gebruik dd-mm-jjjj.')

        # Ensure that the delivery date is at least 2 days ahead of today
        today = datetime.today().date()
        min_date = today + timedelta(days=2)

        if delivery_date < min_date:
            raise ValidationError(
                'De bezorgdatum moet minimaal 2 dagen vanaf vandaag zijn.')

        return delivery_date

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        issuer_id = cleaned_data.get('issuer_id')

        if payment_method == 'ideal' and not issuer_id:
            raise ValidationError({
                'issuer_id': 'Issuer ID is verplicht als de betaalmethode iDEAL is.'
            })

        return cleaned_data
