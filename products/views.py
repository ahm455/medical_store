from django.shortcuts import render,redirect
from .models import Medicine, ordereditems
from .forms import medicineForm,orderedForm


def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

def order_list(request):
    orders = ordereditems.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def add_medicine(request):
    if request.method == 'POST':
            form = medicineForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('medicine_list')
    else:
        form=medicineForm()        
    return render(request,'add_medicine.html',{'form':form})


def add_order(request):
    if request.method == 'POST':
        form = orderedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
            form=orderedForm()         
    return render(request,'add_order.html',{'form':form})        

def dashboard(request):
    return render(request,'dashboard.html')    