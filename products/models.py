from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100)
    potency = models.CharField(max_length=20)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.medicine_name} ({self.potency})"


class Stock(models.Model):
    medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def is_low_stock(self):
        return self.quantity < 10

    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.quantity} units"


class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    PAYMENT_STATUS = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ]

    PAYMENT_METHOD = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Online', 'Online'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Unpaid')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    
    def update_total(self):
        total = self.ordereditem_set.aggregate(total=Sum('total_price'))['total'] or 0
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.customer}"


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit_per_item = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.medicine:
            self.selling_price = self.medicine.selling_price

        if self.quantity and self.selling_price:
            self.total_price = self.quantity * self.selling_price

        if self.medicine:
            self.profit_per_item = (self.selling_price - self.medicine.cost_price) * self.quantity

        super().save(*args, **kwargs)

        stock_obj = Stock.objects.get(medicine=self.medicine)
        stock_obj.quantity -= self.quantity
        stock_obj.save()

        self.order.update_total()

    def delete(self, *args, **kwargs):
        stock_obj = Stock.objects.get(medicine=self.medicine)
        stock_obj.quantity += self.quantity
        stock_obj.save()

        super().delete(*args, **kwargs)

        self.order.update_total()

    def __str__(self):
        return f"{self.medicine} x {self.quantity}"


class Profit(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    profit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_profit(self):
        items = self.order.ordereditem_set.all()

        total_cost = sum(item.medicine.cost_price * item.quantity for item in items)
        total_sell = sum(item.total_price for item in items)

        self.profit_amount = total_sell - total_cost
        self.save()

    def __str__(self):
        return f"Profit for Order {self.order.id}: {self.profit_amount}"