from django.contrib import admin
from .models import Cliente, Categoria, Producto, Venta, DetalleVenta

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'activo', 'fecha_registro']
    list_filter = ['activo', 'fecha_registro']
    search_fields = ['nombre', 'email']
    list_editable = ['activo']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo']
    list_filter = ['categoria', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    readonly_fields = ['subtotal']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'vendedor', 'fecha', 'total', 'estado']
    list_filter = ['estado', 'fecha', 'vendedor']
    search_fields = ['cliente__nombre', 'vendedor__username']
    readonly_fields = ['total']
    inlines = [DetalleVentaInline]