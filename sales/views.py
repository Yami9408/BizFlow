from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Products


def dashboard(request):
    context = {
        'total_ventas':  0,
        'total_productos': Products.objects.filter(
            active=True, stock__gt=0).count(),
        'ventas_recientes': 0
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
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'sales/products.html', context)
