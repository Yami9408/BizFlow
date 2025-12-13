from django.shortcuts import render
from .models import Products


def dashboard(request):
    context = {
        'total_ventas':  0,
        'total_clientes': 0,
        'total_productos': Products.objects.filter(active=True).count(),
        'ventas_recientes': 0
    }
    return render(request, 'ventas/dashboard.html', context)


def list_products(request):
    products = Products.objects.filter(active=True)

    context = {
        'products': products,
    }
    return render(request, 'ventas/productos.html', context)
