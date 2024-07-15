from django import forms
from .models import Account, Transaction

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['sender', 'receiver', 'amount']

        def clean_amount(self):
            print('hello')
            # check the balance validation for sender account
            if self.cleaned_data['amount'] == 0:
                return 0
            return 1

