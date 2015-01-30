# What is house manager
It's a small django application that runs on top of the Raspberry Pi that is used as... a house manager.  
I wrote the app to have some Django-fun but also, because having roommates requires some management.  
This helps noting down groceries spending and bills.
***

Jquery and Boostrtap used heavily for fast phase development.

# Bootstrap it

Requirements:
* [Django 1.7](https://docs.djangoproject.com/en/1.7/releases/1.7.1/),
* [Sqlite3](https://www.sqlite.org/),
* [django-autofixture](https://github.com/gregmuellegger/django-autofixture),
* [Pip](https://bootstrap.pypa.io/get-pip.py)
* Python 2.7,
* [Virtualenv](https://virtualenv.pypa.io/en/latest/)

1. Open a terminal (or git bash) and clone this project:
<pre> git clone git@github.com:freyWill/house_manager.git </pre>
2. Change directory in your terminal inside the project:
<pre>cd (yourpath)/house_manager</pre>

3. Setup virtual environment
<pre>virtualenv env</pre>
4. Install requirements, create migrations, create dummy data, run it
<pre>
source env/bin/activate &&
pip install django==1.7.1 &&
pip install django-autofixture &&
python manage.py migrate &&
python manage.py createsuperuser # create your superuser account
</pre>
5. Put username email and password for the admin.
6. Run server with `python manage.py runserver` and visit [Localhost's admin panel](localhost:8000/admin). From there, create few fake users.
7. Load dummy data
<pre>
  python manage.py loadtestdata spending.Person:1 &&
  python manage.py loadtestdata spending.Deposit:10 &&
  python manage.py loadtestdata spending.MonthlyBill:10 &&
  python manage.py loadtestdata spending.Purchase:10 &&
  python manage.py loadtestdata spending.Withdraw:10
</pre>

>Keep in mind that if you are logged in with an account that does not have a person associated with you, the index will complain.
Make sure to create a Person profile for the root account as well.

Now run server with `python manage.py runserver` and open http://localhost:8000 & enjoy :) !
