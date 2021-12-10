from django.contrib import admin

# Register your models here.
from pstore.models import ItemCart, Order

admin.site.register(ItemCart)
admin.site.register(Order)

