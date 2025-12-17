from datetime import datetime, time, timezone, timedelta
from django.db.models import Sum, Avg
from decimal import Decimal
from django.shortcuts import render
from .models import Products, Debts, Sales
from .utils import get_paginator


def dashboard(request):
    date_from = datetime.now(timezone.utc) - timedelta(days=5)
    resent_sales = Sales.objects.filter(
        created_at__gte=date_from).order_by('-created_at')[:5]

    # Métricas financieras separadas
    total_ventas = Sales.objects.aggregate(
        total=Sum('total_amount'))['total'] or 0
    avg_sale = Sales.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0
    total_sales_count = Sales.objects.count()

    # Margen promedio de productos
    data = Products.objects.filter(active=True).only('profit', 'stock')
    avg_margin = sum(
        (product.profit * product.stock)
        for product in data
    ) * Decimal(0.75)

    context = {
        'total_ventas': total_ventas,
        'total_productos': Products.objects.filter(
            active=True, stock__gt=0).count(),
        'pending_debts': Debts.objects.filter(
            status="pending"
        ).count(),
        'total_debts': Debts.objects.filter().count(),
        'ventas_recientes': bool(resent_sales),
        'recente_sales': resent_sales,
        'avg_sale': avg_sale,
        'total_sales_count': total_sales_count,
        'avg_margin': avg_margin
    }
    return render(request, 'sales/dashboard.html', context)


def list_products(request):
    products = Products.objects.filter(active=True).order_by('-created_at')

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
        if status == 'halfp':
            debts = debts.filter(paid_amount__gt=0, status="pending")
        else:
            debts = debts.filter(status=status)

    context = get_paginator(request, debts, "debts", page_size=12)
    return render(request, 'sales/debts.html', context)


def list_sales(request):
    sales = Sales.objects.all().order_by('-created_at')

    # Filtro por búsqueda en notas
    search = request.GET.get('search')
    if search:
        sales = sales.filter(notes__icontains=search)

    # Filtro por fecha desde
    date_from = request.GET.get('date_from')
    if date_from:
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        sales = sales.filter(created_at__gte=date_from)

    # Filtro por fecha hasta
    date_to = request.GET.get('date_to')
    if date_to:
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
        date_to = datetime.combine(date_to.date(), time.max)
        sales = sales.filter(created_at__lte=date_to)

    context = get_paginator(request, sales, "sales", page_size=12)
    return render(request, 'sales/sales.html', context)


def reports_view(request):
    return render(request, 'sales/reports.html', {})
