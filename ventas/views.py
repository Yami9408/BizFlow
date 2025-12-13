from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Cliente, Producto, Venta, DetalleVenta, Categoria

def dashboard(request):
    context = {
        'total_ventas': Venta.objects.filter(estado='completada').aggregate(Sum('total'))['total__sum'] or 0,
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'total_productos': Producto.objects.filter(activo=True).count(),
        'ventas_recientes': Venta.objects.order_by('-fecha')[:5]
    }
    return render(request, 'ventas/dashboard.html', context)

def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    context = {
        'productos': productos,
        'categorias': categorias
    }
    return render(request, 'ventas/productos.html', context)

def lista_clientes(request):
    clientes = Cliente.objects.filter(activo=True)
    return render(request, 'ventas/clientes.html', {'clientes': clientes})

def lista_ventas(request):
    ventas = Venta.objects.order_by('-fecha')
    return render(request, 'ventas/ventas.html', {'ventas': ventas})

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    context = {
        'venta': venta,
        'detalles': detalles
    }
    return render(request, 'ventas/detalle_venta.html', context)