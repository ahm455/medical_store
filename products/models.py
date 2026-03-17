from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    phone=models.CharField(max_length=20)

    def __str__(self):
            return str(self.name)

class Medicine(models.Model):
    medicine_name=models.CharField(max_length=100)
    potency=models.CharField(max_length=20)
    cost_price=models.DecimalField(max_digits=10, decimal_places=2)
    selling_price=models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.medicine_name} ({self.potency})"

status_choices = [
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
]

class order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL ,null=True)
    medicine=models.ManyToManyField(Medicine, through='ordereditems')
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20, choices=status_choices, default='Pending')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profit.objects.create(order=self)

    def __str__(self):
        return str(self.customer) 

class ordereditems(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.medicine:
            self.selling_price = self.medicine.selling_price
                
        if self.quantity and self.selling_price:
            self.total_price = self.quantity * self.selling_price

        super().save(*args, **kwargs)
class stock(models.Model):
    medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def order_Stock(self, *args, **kwargs):
        if self.medicine:
            self.quantity = self.quantity - self.medicine.ordereditems_set.aggregate(total=models.Sum('quantity'))['total'] or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.quantity} units"

class profit(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    profit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        items = self.order.medicine.all()

        total_cost_price = sum(
            item.medicine.cost_price * item.quantity for item in items
        )

        total_selling_price = sum(
            item.selling_price * item.quantity for item in items
        )

        self.profit_amount = total_selling_price - total_cost_price

        super().save(*args, **kwargs)
    def __str__(self):
        return f"Profit for Order {self.order.id}: {self.profit_amount}"