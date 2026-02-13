from django.forms import ModelForm
from django import forms
# from . import models
from bankaccount.models import BankAccount

class LoginForm(forms.Form):
    username = forms.CharField(max_length=35, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=25, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class AccountForm(ModelForm):
    account_type = forms.ChoiceField(required=True, choices=(("1", "Checking"), ("2", "Savings"), ("3", "Investment")))
    account_name = forms.CharField(max_length=35, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Account or Institution Name'}))
    balance = forms.DecimalField(decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Balance (Can be $0.00'}))

    class Meta:
        model = BankAccount
        fields = ('account_type', 'account_name', 'balance')
        widgets = {
            'account_type': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'account_name': forms.TextInput(attrs={
                'class': 'form-input',
                'required': True
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'form-input',
                'required': True,
                'step': '0.01',
                'min': '0'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_name'].required = True
        self.fields['account_type'].required = True
        self.fields['balance'].required = True

