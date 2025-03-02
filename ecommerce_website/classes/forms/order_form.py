from django import forms


class OrderInfoForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email_address = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    salutation = forms.ChoiceField(
        choices=[
            ('Mevr', 'Mevrouw'),
            ('Dhr', 'Meneer'),
            ('Geen van beiden', 'Geen van beiden')
        ],        required=True
    )

    # Delivery Address Fields
    address = forms.CharField(max_length=255, required=True)
    house_number = forms.CharField(max_length=10, required=True)
    city = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(max_length=10, required=True)
    country = forms.CharField(max_length=50, required=True)

    # Billing Address Fields (Optional unless toggled)
    alternate_billing = forms.BooleanField(required=False)
    billing_address = forms.CharField(max_length=255, required=False)
    billing_house_number = forms.CharField(max_length=10, required=False)
    billing_city = forms.CharField(max_length=100, required=False)
    billing_postal_code = forms.CharField(max_length=10, required=False)
    billing_country = forms.CharField(max_length=50, required=False)

    def clean(self):
        cleaned_data = super().clean()
        alternate_billing = cleaned_data.get("alternate_billing")

        # Validate billing address only if toggle is enabled
        if alternate_billing:
            required_fields = ["billing_address", "billing_house_number",
                               "billing_city", "billing_postal_code", "billing_country"]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(
                        field, "This field is required when using a different billing address.")

        return cleaned_data
