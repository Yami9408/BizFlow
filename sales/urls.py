from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.list_products, name='products'),
    path('debts/', views.list_debts, name='debts'),
    path('sales/', views.list_sales, name='sales'),
    path('reports/', views.reports_view, name='reports'),
]
