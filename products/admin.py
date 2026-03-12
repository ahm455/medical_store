from django.contrib import admin
from .models import Customer, Medicine, order, ordereditems

admin.site.register(order)
admin.site.register(Customer)
