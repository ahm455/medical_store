from django.urls import path
from . import views

urlpatterns = [
    path("",views.dashboard,name='dashboard'),
    path("medicine_view",views.medicine_list,name='medicine_list'),
    path("order_view/",views.order_list,name='order_list'),
    path("add_medicine/",views.add_medicine,name='add_medicine'),
    path("add_order/",views.add_order,name='add_order'),
    path("add_customer/",views.add_customer,name='add_customer'),
    path("customer_view/",views.customer_list,name='customer_list'),
    path("profit_report/",views.profit_report,name='profit_report'),
    path("stock_view/",views.stock_list,name='stock_list'),
    path("add_stock/",views.add_stock,name='add_stock'),
    path("mark_as_shipped/<int:order_id>/", views.mark_order_shipped, name='mark_order_shipped'),
    path("mark_as_delivered/<int:order_id>/", views.mark_order_delivered, name='mark_order_delivered'),
    path("update_stock/<int:order_id>/", views.update_stock, name='update_stock'),
]
