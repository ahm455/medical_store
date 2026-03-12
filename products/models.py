from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.IntegerField()

    def __str__(self):
            return str(self.name)

class Medicine(models.Model):
    medicine_name=models.CharField(max_length=100)
    potency=models.CharField(max_length=20)
    def __str__(self):
        return f"{self.medicine_name} ({self.potency})"

class order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL ,null=True)
    medicine=models.ManyToManyField(Medicine, through='ordereditems')

    def __str__(self):
        return str(self.customer) 

class ordereditems(models.Model):
    order=models.ForeignKey('order', on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL ,null=True)
    medicine=models.ForeignKey('Medicine' ,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return f'{self.order}-{self.medicine},{self.quantity}'

