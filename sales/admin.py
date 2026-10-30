from django.contrib import admin, messages
from django.utils.translation import gettext as _
from .models import (
    Products, Debts, DebtItem,
    Sales, SalesItem, Travels
)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'cost_price_usd',
                    'cost_price_mn', 'sale_price_mn', 'usd_rate',
                    'stock', 'active', 'created_at', 'image',
                    'sales_history', 'profit', 'owner']
    list_filter = ['name', 'active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['cost_price_usd',
                     'cost_price_mn', 'sale_price_mn', 'usd_rate',
                     'stock', 'active']
    readonly_fields = ["cost_price_mn", "profit"]

    # Necesario para autocomplete
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term)
        # Filtrar solo productos activos en el autocomplete
        if 'autocomplete' in request.path:
            queryset = queryset.filter(active=True)
        return queryset, use_distinct


class DebtItemInline(admin.TabularInline):
    model = DebtItem
    extra = 0
    autocomplete_fields = ['product']
    fields = ['product', 'quantity', 'unit_price', 'subtotal']
    readonly_fields = ['subtotal']


@admin.register(Debts)
class DebtsAdmin(admin.ModelAdmin):
    inlines = [DebtItemInline]
    list_display = ['client_name', 'total_amount', 'paid_amount', 'due_date',
                    'status', 'description', 'created_at', 'notes', 'pay_date']
    list_filter = ['client_name', 'status', 'created_at']
    search_fields = ['client_name', 'description']

    actions = [
        'pay_debts',
        'revert_payment_debts',
    ]

    def pay_debts(self, request, queryset):
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

    pay_debts.short_description = _('Pagar la Deuda')

    def revert_payment_debts(self, request, queryset):
        """Admin action to enter coordinators section"""
        for debt in queryset:
            debt.revert_payment()

        self.message_user(
            request,
            "Las deudas han sido revertidas",
            level=messages.SUCCESS
        )

    revert_payment_debts.short_description = _('Revertir deuda pagada')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Calcular total después de guardar todos los DebtItems
        form.instance.calculate_total()


class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 0
    autocomplete_fields = ['product']
    fields = ['product', 'quantity', 'unit_price', 'subtotal', 'profit']
    readonly_fields = ['subtotal']


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
        if not form.instance.employee_payment:
            form.instance.set_employee_total()
        form.instance.set_total_amount()
        form.instance.save()


@admin.register(Travels)
class TravelsAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "rate_type", "rate_change"]
