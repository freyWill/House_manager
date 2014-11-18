from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# validators
def validate_deposit(value):
		if value <= 0:
			raise ValidationError("Positive values please !")

def validate_withdraw(value):
	if value <= 0:
			raise ValidationError("Positive values please !")

class Person(models.Model):
	ammount = models.FloatField()
	user = models.OneToOneField(User)

	def __str__(self):
		return self.user.username

class MonthlyBill(models.Model):
	ammount = models.FloatField()
	billType = models.CharField(max_length=200)
	person = models.ForeignKey(Person)
	theDate = models.DateTimeField(default=timezone.now)
	paid = models.BooleanField(default = False)
	confirmed = models.BooleanField(default=False)


class Purchase(models.Model):
	ammount = models.FloatField()
	person = models.ForeignKey(Person)
	description = models.CharField(max_length=220)
	theDate = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.description

class Deposit(models.Model):
	person = models.ForeignKey(Person)
	ammount = models.FloatField(validators=[validate_deposit])
	theDate = models.DateTimeField(default=timezone.now)

class Withdraw(models.Model):
	person = models.ForeignKey(Person)
	ammount = models.FloatField(validators = [validate_withdraw])
	theDate = models.DateTimeField(default=timezone.now)
	
