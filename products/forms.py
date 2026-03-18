from django import forms
from .models import Medicine, OrderedItem, Customer, Order, Stock, Profit
from django.contrib.auth.models import User
from rest_framework import serializers


class medicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'potency', 'cost_price', 'selling_price']


class OrderedItemsForm(forms.ModelForm):
    class Meta:
        model = OrderedItem
        fields = ['customer', 'medicine', 'quantity']

    def create(self, validated_data):
        customer = validated_data.get('customer')
        medicine = validated_data.get('medicine')
        quantity = validated_data.get('quantity')
        order = validated_data.get('order')  # passed from view

        try:
            stock_obj = Stock.objects.get(medicine=medicine)
        except Stock.DoesNotExist:
            raise serializers.ValidationError(f"No stock available for {medicine.medicine_name}")

        if stock_obj.quantity < quantity:
            raise serializers.ValidationError(f"Not enough stock for {medicine.medicine_name}")

        stock_obj.quantity -= quantity
        stock_obj.save()

        ordered_item = OrderedItem.objects.create(
            customer=customer,
            medicine=medicine,
            quantity=quantity,
            selling_price=medicine.selling_price,
            total_price=medicine.selling_price * quantity,
            profit_per_item=(medicine.selling_price - medicine.cost_price) * quantity,
            order=order
        )
        return ordered_item


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_status', 'payment_method', 'status']


from django import forms
from .models import Customer

class customerform(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'age', 'phone']  # no user input

    def save(self, commit=True):
        customer = super().save(commit=False)
        from django.contrib.auth.models import User
        customer.user = User.objects.first()  # assign the same user to all customers
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