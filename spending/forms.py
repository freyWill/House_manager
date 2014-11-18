from django import forms
from spending.models import Purchase, Deposit, Withdraw

class PurchaseForm(forms.ModelForm):
	class Meta:
		model = Purchase
		fields = ['ammount', 'description']

class DepositForm(forms.ModelForm):
	class Meta:
		model = Deposit
		fields = ['ammount']

class WithdrawForm(forms.ModelForm):
	class Meta:
		model = Withdraw
		fields = ['ammount']

class MonthlyPaymentForm(forms.Form):

	options = (
            ("utility", "Utility bills"),
            ("internet", "Internet Bills"),
            )
	billType = forms.ChoiceField(choices=options)
	ammount = forms.FloatField()