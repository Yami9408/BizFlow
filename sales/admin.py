from django.contrib import admin
from .models import Products, Debts, DebtItem


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'cost_price_usd',
                    'cost_price_mn', 'sale_price_mn', 'usd_rate',
                    'stock', 'active', 'created_at', 'image', 'sales_history']
    list_filter = ['name', 'active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['cost_price_usd',
                     'cost_price_mn', 'sale_price_mn', 'usd_rate',
                     'stock', 'active']
    readonly_fields = ["cost_price_mn"]


class DebtItemInline(admin.TabularInline):
    model = DebtItem
    extra = 0


@admin.register(Debts)
class DebtsAdmin(admin.ModelAdmin):
    inlines = [DebtItemInline]
    list_display = ['client_name', 'total_amount', 'paid_amount', 'due_date',
                    'status', 'description', 'created_at', 'notes', 'pay_date']
    list_filter = ['client_name', 'status', 'created_at']
    search_fields = ['client_name', 'description']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Calcular total después de guardar todos los DebtItems
        form.instance.calculate_total()
        # form.instance.save()
