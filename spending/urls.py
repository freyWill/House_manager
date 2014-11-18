from django.conf.urls import url


urlpatterns = [
	url(r'^$', 'spending.views.home', name='index'),
	url(r'deduct/', 'spending.views.confirmDeduct', name='confirmDeduct'),
	url(r'profile/(?P<username>\w+)/', 'spending.views.profile', name='profile'),
	url(r'addExpense/', 'spending.views.addExpense', name='addExpense'),
	url(r'deposit/', 'spending.views.deposit', name='deposit'),
	url(r'withdraw/', 'spending.views.withdraw', name='withdraw'),
	url(r'orderBills/', 'spending.views.orderBills', name='orderBills'),
	url(r'viewDuePayments/', 'spending.views.viewDuePayments', name='viewDuePayment'),
	url(r'claimPaid/(?P<bill_id>\d+)/', 'spending.views.claimPaid', name='claimPaid'),
	url(r'confirmPaid/(?P<bill_id>\d+)/', 'spending.views.confirmPaid', name='confirmPaid'),
	url(r'paybackView/', 'spending.views.paybackView', name='paybackView'),
	url(r'remove/product/(?P<product_id>\d+)', 'spending.views.deletePurchase', name='removeProduct'),

]