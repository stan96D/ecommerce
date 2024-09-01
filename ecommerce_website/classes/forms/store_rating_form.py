from django import forms
from ecommerce_website.models import StoreRating


class StoreRatingForm(forms.ModelForm):
    class Meta:
        model = StoreRating
        fields = ['title', 'description', 'stars']
