from django.urls import path
from . import views

urlpatterns = [
    path("",views.dashboard,name='dashboard'),
    path("medicine_view",views.medicine_list,name='medicine_list'),
    path("order_view/",views.order_list,name='order_list'),
    path("add_medicine/",views.add_medicine,name='add_medicine'),
    path("add_order/",views.add_order,name='add_order'),
]