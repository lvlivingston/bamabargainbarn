from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    street_address = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=25, required=True)
    state = forms.CharField(max_length=2, required=True)
    ship_zip = forms.CharField(max_length=5, required=True)