from django.forms import ModelForm
from django import forms
from . import models
from bankaccount.models import BankAccount

class LoginForm(forms.Form):
    username = forms.CharField(max_length=35, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=25, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class AccountForm(ModelForm):
    account_type = forms.MultipleChoiceField(choices=(("1", "Checking"), ("2", "Savings"), ("3", "Investment")), required=True)
    account_name = forms.CharField(max_length=35, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Account or Institution Name'}))
    balance = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Balance (Can be $0.00'}))

    class Meta:
        model = BankAccount
        fields = ('account_type', 'account_name', 'balance')
        widgets = {
            'account_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

