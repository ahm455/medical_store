from django.shortcuts import render,redirect
from .models import *
from .forms import *
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone

def dashboard(request):
    return render(request,'dashboard.html')  
def add_medicine(request):
    if request.method == 'POST':
            data = request.POST.dict()
            serializer = medicineForm(data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect('medicine_list')
    else:
        serializer=medicineForm()        
    return render(request,'add_medicine.html',{'serializer':serializer})
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})


def add_order(request):
    if request.method == 'POST':
        data = request.POST.dict()
        serializer = OrderedItemsForm(data=data)
        if serializer.is_valid():
            new_order = order.objects.create(customer=serializer.validated_data['customer'])
            ordered_item = serializer.save(order=new_order, customer=request.user.customer)
            ordered_item.order = new_order
            ordered_item.id = None  # Ensure a new ordereditems instance is created
            ordered_item.save()
            return redirect('order_list')
    else:
            serializer=OrderedItemsForm()         
    return render(request,'add_order.html',{'serializer':serializer})          
def order_list(request):
    orders = ordereditems.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


def add_customer(request):
    if request.method == 'POST':    
        serializer = customerForm(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('customer_list') 
    else:
        serializer = customerForm()
    return render(request, 'add_customer.html', {'serializer': serializer})


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def profit_report(request):
    profits = profit.objects.all()
    weekly_profits = profit.objects.filter(
    order__created_at__gte=timezone.now() - timedelta(days=7)
    )

    monthly_profits = profit.objects.filter(order__created_at__gte=timezone.now() - timedelta(days=30))
    return render(request, 'profit.html', {'profits': profits, 'weekly_profits': weekly_profits, 'monthly_profits': monthly_profits})

def add_stock(request):
    if request.method == 'POST':
        serializer = stockForm(data=request.POST)
        if serializer.is_valid():
            serializer.save()  # Stock logic is already handled in serializer
            return redirect('stock_list')
    else:
        serializer = stockForm()

    return render(request, 'add_stock.html', {'serializer': serializer})

def stock_list(request):
    stocks = stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})     

def mark_order_shipped(request, order_id):
    try:
        order_instance = order.objects.get(id=order_id)
        order_instance.status = 'Shipped'
        order_instance.save()
        return redirect('order_list')
    except order.DoesNotExist:
        return redirect('order_list')

def mark_order_delivered(request, order_id):
    try:
        order_instance = order.objects.get(id=order_id)
        order_instance.status = 'Delivered'
        order_instance.save()
        return redirect('order_list')
    except order.DoesNotExist:
        return redirect('order_list')

def update_stock(request, stock_id):
    try:
        stock_instance = stock.objects.get(id=stock_id)
    except stock.DoesNotExist:
        return redirect('stock_list')

    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        if new_quantity is not None:
            stock_instance.quantity = new_quantity
            stock_instance.save()
            return redirect('stock_list')

    return render(request, 'update_stock.html', {'stock': stock_instance})