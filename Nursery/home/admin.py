from django.contrib import admin
from .models import *
from account.models import *
from cart.models import payment




# Register your models here.
class catg_plantadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(categ_plants,catg_plantadmin)

class PlantAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ['name','mob_num','photo','email','nursery_address']
    exclude = ['password1']
admin.site.register(plant_admin,PlantAdminReadOnly)
admin.site.register(add_plants)
admin.site.register(Feedback)
class PaymentAdmin(admin.ModelAdmin):

    readonly_fields=['user', 'account_number', 'name']
    exclude = ['expiry_month','expiry_date','cvv']

admin.site.register(payment,PaymentAdmin,)

class contact_view(admin.ModelAdmin):
    readonly_fields=['name', 'email', 'subject','message']

admin.site.register(Contact,contact_view)
#admin.site.register(items_plant)