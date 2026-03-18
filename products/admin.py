from django.contrib import admin
from .models import Customer, Medicine, Order, OrderedItem

admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(Customer)
