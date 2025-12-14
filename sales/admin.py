from django.contrib import admin
from .models import Products, Debt


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'cost_price_usd',
                    'cost_price_mn', 'sale_price_mn', 'usd_rate',
                    'stock', 'active', 'create_At', 'image', 'sales_history']
    list_filter = ['name', 'active', 'create_At']
    search_fields = ['name', 'description']
    list_editable = ['cost_price_usd',
                     'cost_price_mn', 'sale_price_mn', 'usd_rate',
                     'stock', 'active']
    readonly_fields = ["cost_price_mn"]


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'product', 'quantity',
                    'total_amount', 'paid_amount', 'due_date',
                    'status', 'description', 'created_at', 'notes', 'pay_date']
    list_filter = ['client_name', 'status', 'created_at']
    search_fields = ['client_name', 'description']
