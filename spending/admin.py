from django.contrib import admin
from spending.models import Person, Purchase, Deposit, Withdraw, MonthlyBill
# Register your models here.

class PurchaseAdmin(admin.ModelAdmin):
	list_display = ['description', 'person', 'ammount', "theDate"]

class DepositAdmin(admin.ModelAdmin):
	list_display = ['person', 'ammount', "theDate"]

class MonthlyBillAdmin(admin.ModelAdmin):
	list_display = ['person', 'ammount', 'theDate', 'billType', 'paid', 'confirmed']

admin.site.register(Person)
admin.site.register(MonthlyBill, MonthlyBillAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdraw, DepositAdmin)
