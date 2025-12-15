from django.shortcuts import render
from .models import Products, Debts
from .utils import get_paginator


def dashboard(request):
    context = {
        'total_ventas':  0,
        'total_productos': Products.objects.filter(
            active=True, stock__gt=0).count(),
        'pending_debts': Debts.objects.filter(
            status="pending"
        ).count(),
        'total_debts': Debts.objects.filter().count()
    }
    return render(request, 'sales/dashboard.html', context)


def list_products(request):
    products = Products.objects.filter(active=True)

    # Filtro por búsqueda de nombre
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

    # Filtro por precio mínimo
    min_price = request.GET.get('min_price')
    if min_price:
        products = products.filter(sale_price_mn__gte=min_price)

    # Filtro por precio máximo
    max_price = request.GET.get('max_price')
    if max_price:
        products = products.filter(sale_price_mn__lte=max_price)

    # Filtro por Stock
    active_stock = request.GET.get('active_stock')
    if active_stock:
        products = products.filter(stock__gt=0)

    # Optimizar consulta
    products = products.only("id", "name", "image", "stock",
                             "description", "sale_price_mn").order_by('name')

    # Paginación
    context = get_paginator(request, products, "products", page_size=12)
    return render(request, 'sales/products.html', context)


def list_debts(request):
    debts = Debts.objects.filter().order_by('-created_at')
    search = request.GET.get('search')
    if search:
        debts = debts.filter(client_name__icontains=search)
    status = request.GET.get('status')
    if status:
        debts = debts.filter(status=status)

    context = get_paginator(request, debts, "debts", page_size=12)
    return render(request, 'sales/debts.html', context)
