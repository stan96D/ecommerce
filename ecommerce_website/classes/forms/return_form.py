from django import forms


class ReturnForm(forms.Form):
    # Define the fields from your QueryDict with validation
    return_reason = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Je reden om te retourneren..."}
        ),
        required=True,
        max_length=1000,
        label="Retourreden",

    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label="Voornaam",
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        label="Achternaam",
    )
    email_address = forms.EmailField(
        required=True,
        label="E-mailadres",
    )
    address = forms.CharField(
        max_length=255,
        required=True,
        label="Adres",
    )
    house_number = forms.CharField(
        max_length=10,
        required=True,
        label="Huisnummer",
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        label="Plaats",
    )
    postal_code = forms.RegexField(
        regex=r"^\d{4}\s?[A-Z]{2}$",
        required=True,
        label="Postcode",
        error_messages={
            "invalid": "Voer een geldige Nederlandse postcode in, bijv. 1234 AB."
        },
    )
    country = forms.ChoiceField(
        choices=[
            ("Nederland", "Nederland"),
            ("België", "België"),
        ],
        required=True,
        label="Land",
    )
    phone = forms.RegexField(
        regex=r"^\+?[0-9]{8,15}$",
        required=True,
        label="Telefoonnummer",
        error_messages={"invalid": "Voer een geldig telefoonnummer in."},
    )

    # Duplicate fields for billing address with a prefix
    billing_address = forms.CharField(
        max_length=255,
        required=False,  # Optional if different billing isn't mandatory
        label="Factuuradres",
    )
    billing_house_number = forms.CharField(
        max_length=10,
        required=False,
        label="Factuur huisnummer",
    )
    billing_city = forms.CharField(
        max_length=100,
        required=False,
        label="Factuur plaats",
    )
    billing_postal_code = forms.RegexField(
        regex=r"^\d{4}\s?[A-Z]{2}$",
        required=False,
        label="Factuur postcode",
        error_messages={
            "invalid": "Voer een geldige Nederlandse postcode in, bijv. 1234 AB."
        },
    )
    billing_country = forms.ChoiceField(
        choices=[
            ("Nederland", "Nederland"),
            ("België", "België"),
        ],
        required=False,
        label="Factuurland",
    )
    billing_phone = forms.RegexField(
        regex=r"^\+?[0-9]{8,15}$",
        required=False,
        label="Factuur telefoonnummer",
        error_messages={"invalid": "Voer een geldig telefoonnummer in."},
    )

    # Field for the billing toggle
    alternative_billing = forms.ChoiceField(
        choices=[("true", "True"), ("false", "False")],
        required=True,
        label="Afwijkend factuuradres",
        widget=forms.HiddenInput(),  # Hidden input if this is controlled by JavaScript
    )
