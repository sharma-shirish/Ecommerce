from django import forms

PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 Main St'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apartment or suite'
    }))
    # country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
    #    'class': 'custom-select d-block w-100'
    # }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT)
