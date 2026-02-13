from django import forms

class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
    note = forms.CharField(max_length=255, required=False)

