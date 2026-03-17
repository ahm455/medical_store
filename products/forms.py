from django import forms
from .models import Medicine, ordereditems,Customer,order,stock,profit
from django.contrib.auth.models import User
from rest_framework import serializers


class medicineForm(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'potency', 'cost_price', 'selling_price']


class OrderedItemsForm(serializers.ModelSerializer):
    class Meta:
        model = ordereditems
        fields = ['customer', 'medicine', 'quantity']

class OrderForm(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = ['customer']


class customerForm(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['name', 'age', 'phone', 'username', 'email', 'password']

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, email=email, password=password)

        customer = Customer.objects.create(user=user, **validated_data)
        return customer

from rest_framework import serializers
from .models import stock

class stockForm(serializers.ModelSerializer):
    class Meta:
        model = stock
        fields = ['medicine', 'quantity']

    def save(self, *args, **kwargs):
        medicine = self.validated_data['medicine']
        quantity = self.validated_data['quantity']

        try:
            stock_instance = stock.objects.get(medicine=medicine)
            stock_instance.quantity += quantity
            stock_instance.save()
            return stock_instance
        except stock.DoesNotExist:
            return super().save(*args, **kwargs)