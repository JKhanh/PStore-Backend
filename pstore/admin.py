from django.contrib import admin

# Register your models here.
from pstore.models import Product, Customer, ItemCart, Order, Review

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(ItemCart)
admin.site.register(Order)
admin.site.register(Review)

