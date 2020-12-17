from django import forms

class NegotiateForm(forms.Form):
    client_price = forms.CharField(label='Your price', max_length=100)
