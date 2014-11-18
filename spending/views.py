from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from spending.models import Person, Purchase, Deposit, Withdraw, MonthlyBill
from spending.forms import PurchaseForm, DepositForm, WithdrawForm, MonthlyPaymentForm
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def check_budget():
	users = Person.objects.all()
	deduction = True
	for user in users:
		if user.ammount > -10:
			deduction = False
	return deduction

def deduct_total():
	persons = Person.objects.all()
	lowest = persons[0].ammount
	agreed = 0
	for person in persons:
		if person.ammount > lowest and person.ammount < 0:
			lowest = user.ammount
		if person.deduct == True:
			agreed+=1
	print agreed
	if agreed != 4:
		return
	else:
		for person in persons:
			person.ammount += abs(lowest)
			person.deduct = False
			person.save()


@login_required
def home(request):
	deduction = check_budget()
	if deduction:
		deduct_total()

	people = Person.objects.all()
	total_ammount = 0
	for person in people:
		total_ammount = person.ammount

	data = {

		'profile' : Person.objects.get(user = request.user),
		'total_ammount':total_ammount,
		'user':request.user,
		'deduction' : deduction,
		'users' : User.objects.all().exclude(username = 'root'),
		'purchases' : Purchase.objects.all().order_by('-theDate'),
		'deposits' : Deposit.objects.all().order_by('-theDate'),
		'withdrawals' : Withdraw.objects.all().order_by('-theDate'),

		}

	return render_to_response("index.html", data)

@login_required
def profile(request, username):
	if request.user.is_authenticated():
		# fetch person object
		currentPerson = Person.objects.get(user__username = username)

		parameters = {
			'user':request.user,
			'name' : username,
			'profile' : Person.objects.get(user__username = username),
			'purchases' : Purchase.objects.filter(person=currentPerson),
			'deposits' : Deposit.objects.filter(person = currentPerson),
			'withdrawals' : Withdraw.objects.filter(person = currentPerson),
		}
		return render_to_response("profile.html", parameters)
	else:
		return redirect("my_login")

@login_required
def addExpense(request):
	c = {}
	c.update(csrf(request))

	currentPerson = Person.objects.get(user = request.user) # current logged in person

	if request.method == "POST":
		form = PurchaseForm(request.POST)
		if form.is_valid():
			# if user input is valid, make a new purchase
			newPurchase = form.save(commit=False)
			newPurchase.person = currentPerson
			newPurchase.save()

			#now decrease that person's budget

			currentPerson.ammount -= newPurchase.ammount
			currentPerson.save()

			message = {
				"expense" : newPurchase.ammount,
				'profile' : Person.objects.get(user__username = request.user.username),
				"notification" : True,
				"description" : newPurchase.description,
				"user" : request.user,
				'users' : User.objects.all().exclude(username = 'root'),
			}

			return render_to_response("index.html", message)	
	else:
		form = PurchaseForm()

	data = {
		'form' : form,
		'token': c,
		'user':request.user,
		'profile' : Person.objects.get(user = request.user),


	}

	return render_to_response("forms/purchase_form.html", data, context_instance=RequestContext(request) )

@login_required
def deletePurchase(request, product_id):

	data = {
		'user' : request.user,
		'users' : User.objects.all().exclude(username = 'root'),
 	}

	productToDelete = Purchase.objects.get(pk=product_id)
	owner = Person.objects.get(user = request.user)
	
	owner.ammount += productToDelete.ammount
	productToDelete.delete()
	owner.save()

	if productToDelete.person.pk == owner.pk:
		return render_to_response("index.html", data)
	else:
		return render_to_response("This product does not belong to you, get back <a href='../../../'>here</a>")

@login_required
def deposit(request):
	if not request.user.is_authenticated:
		return redirect("index")

	c = {}
	c.update(csrf(request))

	if request.method == "POST":
		form = DepositForm(request.POST)
		if form.is_valid():
			currentPerson = Person.objects.get(user=request.user)

			newDeposit = Deposit()
			newDeposit = form.save(commit=False)
			newDeposit.person = currentPerson
			
			currentPerson.ammount += newDeposit.ammount

			newDeposit.save()
			currentPerson.save()
			return redirect("index")
	else:
		form = DepositForm()

	data = {
		"form" : form,
		"token": c,
		'profile' : Person.objects.get(user = request.user),

	}
	return render_to_response("forms/deposit_form.html", data, context_instance=RequestContext(request))

@login_required
def withdraw(request):
	if not request.user.is_authenticated:
		redirect("index")

	c = {}
	c.update(csrf(request))

	if request.method == "POST":
		form = WithdrawForm(request.POST)
		if form.is_valid():
			currentPerson = Person.objects.get(user=request.user)

			newWithdraw = form.save(commit=False)
			newWithdraw.person = currentPerson
			
			currentPerson.ammount -= newWithdraw.ammount

			newWithdraw.save()
			currentPerson.save()
			return redirect("index")
	else:
		form = WithdrawForm()

	data = {
		"form" : form,
		"token": c,
		'profile' : Person.objects.get(user = request.user),

	}
	return render_to_response("forms/withdraw_form.html", data, context_instance=RequestContext(request))

def confirmDeduct(request):
	me = Person.objects.get(user = request.user)
	me.deduct = True
	me.save()
	return redirect("index")

@login_required
def orderBills(request):

	if request.user.username != "daniel":
		return redirect("index")

	c = {}
	c.update(csrf(request))
	
	if request.method == "POST":
		form = MonthlyPaymentForm(request.POST)
		if form.is_valid():
			everyone = Person.objects.all().exclude(user__username="daniel")

			# peopleToBill = peopleToBill.exclude(user__username="daniel")
			for thePerson in everyone:
				bill = MonthlyBill(ammount=(form.cleaned_data['ammount']/4), billType=form.cleaned_data['billType'], person=thePerson)
				bill.save()
			return redirect("index")
	else:
		form = MonthlyPaymentForm()

	data = {
		'user':request.user,
		'profile' : Person.objects.get(user = request.user),
		'token' : c,
		'form': form,
	}

	return render_to_response("forms/order_payment_form.html", data, context_instance = RequestContext(request))

@login_required
def viewDuePayments(request):
	# get person
	currentPerson = Person.objects.get(user= request.user)
	dueBills = MonthlyBill.objects.filter(person = currentPerson, confirmed=False)
	pastBills = MonthlyBill.objects.filter(person = currentPerson, confirmed=True)
	if dueBills is None:
		dueBills = "asd"
	data = {
		'bills' : dueBills,
		'pastBills' : pastBills,
		'user':request.user,
		'profile' : Person.objects.get(user = request.user),
	}

	return render_to_response("view_due_payments.html", data)

@login_required
def claimPaid(request, bill_id):
	theBill = MonthlyBill.objects.get(pk=bill_id, person__user=request.user)
	theBill.paid = True
	theBill.save()
	return redirect("index")

def confirmPaid(request, bill_id):
	theBill = MonthlyBill.objects.get(pk=bill_id)
	theBill.confirmed = True
	theBill.save()
	return redirect("index")

@login_required
def paybackView(request):
	notConfirmed = MonthlyBill.objects.filter(paid=True, confirmed=False)
	notPaid = MonthlyBill.objects.filter(paid=False, confirmed=False)
	oldTransactions = MonthlyBill.objects.filter(paid=True, confirmed=True)

	data = {
		'notConfirmed' : notConfirmed,
		'notPaid' : notPaid,
		'oldTransactions' : oldTransactions,
		'user':request.user,
		'profile' : Person.objects.get(user = request.user),
	}

	return render_to_response("payback.html", data)

def createUsers(request):

	try:
		theSuperman = User.objects.get(username='root')
	except User.DoesNotExist: 
		my_admin = User.objects.create_superuser('root', 'myemail@test.com', 'toor')
		my_admin.save()

	plamen = User.objects.create_user('plamen', 'lennon@thebeatles.com', 'plamen')
	daniel = User.objects.create_user('daniel', 'lennon@thebeatles.com', 'daniel')
	alek = User.objects.create_user('alek', 'lennon@thebeatles.com', 'alek')
	dennis = User.objects.create_user('dennis', 'lennon@thebeatles.com', 'dennis')

	plamenPerson = Person(user=plamen, ammount=0)
	danielPerson = Person(user=daniel, ammount=0)
	alekPerson = Person(user=alek, ammount=0)
	dennisPerson = Person(user=dennis, ammount=0)

	plamen.save()
	daniel.save()
	alek.save()
	dennis.save()

	plamenPerson.save()
	danielPerson.save()
	alekPerson.save()
	dennisPerson.save()

	return redirect("index")
