from django.contrib import admin, messages
from django.utils.translation import gettext as _
from .models import (
    Products, Debts, DebtItem,
    Sales, SalesItem
)


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
    readonly_fields = ["cost_price_mn", "profit"]


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

    actions = [
        'page_debts'
    ]

    def page_debts(self, request, queryset):
        """Admin action to enter coordinators section"""
        get_total_to_paid = 0
        for debt in queryset:
            get_total_to_paid += debt.get_total_to_paid()
            debt.pay()

        self.message_user(
            request,
            f"Las deudas han sido pagadas: {get_total_to_paid} ha pagar",
            level=messages.SUCCESS
        )

    page_debts.short_description = _('Pagar la Deuda')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Calcular total después de guardar todos los DebtItems
        form.instance.calculate_total()


class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 0


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    inlines = [SalesItemInline]
    list_display = ['total_amount', 'created_at', 'notes', 'card_amount',
                    'employee_payment', 'employee_percent',
                    'total_profit']
    list_filter = ['created_at']
    search_fields = ['notes']
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.set_employee_total()
        form.instance.set_total_amount()
        form.instance.save()
        
