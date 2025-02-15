from django import forms
from django.core.validators import RegexValidator


class OrderForm(forms.Form):
    SALUTATION_CHOICES = [
        ('Dhr', 'Dhr'),  # Mr.
        ('Mevr', 'Mevr'),  # Ms.
        ('Geen van beiden', 'Geen van beiden'),  # None of the above
    ]

    salutation = forms.ChoiceField(choices=SALUTATION_CHOICES, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email_address = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=15,
        required=True,
        validators=[RegexValidator(
            r'^\+?\d{7,15}$', message="Enter a valid phone number.")]
    )

    address = forms.CharField(max_length=255, required=True)
    house_number = forms.CharField(max_length=10, required=True)
    city = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(
        max_length=10,
        required=True,
        validators=[RegexValidator(
            r'^\d{4,10}$', message="Enter a valid postal code.")]
    )
    country = forms.CharField(max_length=100, required=True)

    different_billing = forms.BooleanField(required=False)

    billing_address = forms.CharField(max_length=255, required=False)
    billing_house_number = forms.CharField(max_length=10, required=False)
    billing_city = forms.CharField(max_length=100, required=False)
    billing_postal_code = forms.CharField(
        max_length=10,
        required=False,
        validators=[RegexValidator(
            r'^\d{4,10}$', message="Enter a valid postal code.")]
    )
    billing_country = forms.CharField(max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()
        different_billing = cleaned_data.get("different_billing")

        if different_billing:  # If user has selected different billing
            required_fields = ["billing_address", "billing_house_number",
                               "billing_city", "billing_postal_code", "billing_country"]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(
                        field, "This field is required if different billing is selected.")
        else:
            # Copy shipping address to billing address if different billing is False
            cleaned_data["billing_address"] = cleaned_data.get("address")
            cleaned_data["billing_house_number"] = cleaned_data.get(
                "house_number")
            cleaned_data["billing_city"] = cleaned_data.get("city")
            cleaned_data["billing_postal_code"] = cleaned_data.get(
                "postal_code")
            cleaned_data["billing_country"] = cleaned_data.get("country")

        return cleaned_data
