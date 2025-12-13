from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('productos/', views.lista_productos, name='productos'),
    path('clientes/', views.lista_clientes, name='clientes'),
    path('ventas/', views.lista_ventas, name='ventas'),
    path('ventas/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
]