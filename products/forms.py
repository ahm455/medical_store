from django import forms
from .models import Medicine, OrderedItem, Customer, Order, Stock, Profit
from django.contrib.auth.models import User
from rest_framework import serializers


class medicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'potency', 'cost_price', 'selling_price']

class OrderedItemsForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), empty_label="Select Customer")
    medicine = forms.ModelChoiceField(queryset=Medicine.objects.all(), empty_label="Select Medicine")

    class Meta:
        model = OrderedItem
        fields = ['customer', 'medicine', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'payment_method']


class customerform(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'age', 'phone']

    def save(self, commit=True):
        customer = super().save(commit=False)

        if commit:
            customer.save()
        return customer

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['medicine', 'quantity']

    def save(self, commit=True):
        medicine = self.cleaned_data['medicine']
        quantity = self.cleaned_data['quantity']
        try:
            stock_instance = Stock.objects.get(medicine=medicine)
            stock_instance.quantity += quantity
            stock_instance.save()
            return stock_instance
        except Stock.DoesNotExist:
            return super().save(commit=commit)