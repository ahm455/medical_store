from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import Customer, Medicine, Stock, Order, OrderedItem, Profit
from .forms import customerform, medicineForm, StockForm, OrderedItemsForm, OrderForm
from django.shortcuts import render
from django.db.models import Sum
from .models import Order, Customer, Medicine, Stock
from django.shortcuts import render
from .models import Order, Customer, Medicine, Stock

def dashboard(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    shipped_orders = Order.objects.filter(status='Shipped').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    total_customers = Customer.objects.count()
    total_medicines = Medicine.objects.count()
    stocks = Stock.objects.all()
    weekly_profits = Profit.objects.filter(
        order__created_at__gte=timezone.now() - timedelta(days=7)
    ).aggregate(total_profit=Sum('profit_amount'))['total_profit'] or 0
    monthly_profits = Profit.objects.filter(
        order__created_at__gte=timezone.now() - timedelta(days=30)
    ).aggregate(total_profit=Sum('profit_amount'))['total_profit'] or 0
    total_medicine_value = sum(stock.quantity * stock.medicine.selling_price for stock in stocks)

    context = {
        'weekly_profits': weekly_profits,
        'monthly_profits': monthly_profits,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'total_customers': total_customers,
        'total_medicines': total_medicines,
        'total_medicine_value': total_medicine_value,
    }
    return render(request, 'dashboard.html', context)
def add_customer(request):
    form = customerform(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('customer_list')
    return render(request, 'add_customer.html', {'form': form})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def add_medicine(request):
    form = medicineForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('medicine_list')
    return render(request, 'add_medicine.html', {'form': form})

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

def add_stock(request):
    form = StockForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('stock_list')
    return render(request, 'add_stock.html', {'form': form})

def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})

def update_stock(request, stock_id):
    stock_instance = get_object_or_404(Stock, id=stock_id)
    serializer = StockForm(stock_instance, data=request.POST or None)
    if request.method == 'POST' and serializer.is_valid():
        serializer.save()
        return redirect('stock_list')
    return render(request, 'update_stock.html', {'serializer': serializer})

def add_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        items_form = OrderedItemsForm(request.POST)

        if order_form.is_valid() and items_form.is_valid():
        
            order = order_form.save(commit=False)
            order.customer = items_form.cleaned_data['customer']
            order.save()

    
            item = items_form.save(commit=False)
            item.order = order
            item.customer = order.customer
            item.save()

            profit_record = Profit.objects.create(order=order)
            profit_record.calculate_profit()

            return redirect('order_list')

    else:
        order_form = OrderForm()
        items_form = OrderedItemsForm()

    return render(request, 'add_order.html', {
        'order_form': order_form,
        'items_form': items_form
    })

def order_list(request):
    orders = Order.objects.all()
    if request.method == 'POST':
        for order in orders:
            form = OrderForm(request.POST, instance=order, prefix=f'order_{order.id}')
            if form.is_valid():
                form.save()
        return redirect('order_list')
    order_forms = [{'order': order, 'form': OrderForm(instance=order, prefix=f'order_{order.id}')} for order in orders]
    return render(request, 'order_list.html', {'order_forms': order_forms})

def profit_report(request):
    profits = Profit.objects.all()
    weekly_profits = Profit.objects.filter(
        order__created_at__gte=timezone.now() - timedelta(days=7)
    ).aggregate(total_profit=Sum('profit_amount'))['total_profit'] or 0
    monthly_profits = Profit.objects.filter(
        order__created_at__gte=timezone.now() - timedelta(days=30)
    ).aggregate(total_profit=Sum('profit_amount'))['total_profit'] or 0
    return render(request, 'profit.html', {
        'profits': profits,
        'weekly_profits': weekly_profits,
        'monthly_profits': monthly_profits
    })