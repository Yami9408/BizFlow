from django.contrib import admin
from .models import Products


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
