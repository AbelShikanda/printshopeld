from django import forms
from setuptools import Require


class MpesaPaymentForm(forms.Form):
    phone = forms.CharField(
                            label='Enter Number', 
                            max_length=15,
                            required=True,
                            widget=forms.TextInput(attrs={
                                                            'class': 'form-control', 
                                                            'placeholder': '2547123456789',
                                                            'id': 'number',
                                                            'name': 'number',
                                                            }
                                                    )
                            )
    # price = forms.IntegerField(
    #                         label='Enter Number', 
    #                         required=True,
    #                         widget=forms.NumberInput(attrs={
    #                                                         'type': 'number',
    #                                                         'id': 'num',
    #                                                         'name': 'num',
    #                                                         'value': "",
    #                                                         'class': 'form-control'
    #                                                         }
    #                                                 )
    #                         )