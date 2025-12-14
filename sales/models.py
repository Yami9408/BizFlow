from datetime import datetime, timezone
from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.translation import gettext as _


class Products(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nombre"), db_index=True)
    description = models.TextField(blank=True, verbose_name=_("Descripción"))
    cost_price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=False, blank=False,
        verbose_name=_("Precio de costo USD")
    )
    cost_price_mn = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        # null=False, blank=False,
        verbose_name=_("Precio de costo MN")
    )
    sale_price_mn = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False, blank=False,
        verbose_name=_("Precio de venta MN"),
        db_index=True
    )
    usd_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        help_text="Tipo de cambio USD → moneda local para este producto",
        null=False, blank=False,
        default=500,
        verbose_name=_("Tipo de cambio USD")
    )

    stock = models.PositiveIntegerField(
        default=0, verbose_name=_("Stock"),
        db_index=True)
    image = models.ImageField(
        upload_to='products/', blank=True, null=True,
        verbose_name=_("Imagen")
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_("Activo"), db_index=True)
    create_At = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación")
    )
    sales_history = models.JSONField(
        default=list, blank=True,
        verbose_name=_("Historial de ventas")
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def add_sale(self, quantity):
        if self.stock < quantity:
            raise ValueError("No hay suficiente stock")
        self.stock -= quantity
        # agregar al historial
        self.sales_history.append({
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "quantity": quantity
        })
        print(f"Quedan en stock {self.name}: {self.stock}")
        self.save()

    def save(self, *args, **kwargs):
        self.cost_price_mn = self.cost_price_usd * self.usd_rate
        super().save(*args, **kwargs)


class Debts(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pendiente')),
        ('paid', _('Pagada')),
        ('overdue', _('Vencida')),
    ]

    client_name = models.CharField(
        max_length=100,
        null=False, blank=False,
        verbose_name=_("Nombre del cliente"))

    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name=_("Producto")
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Cantidad")
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Monto total")
    )
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Monto pagado")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación"))
    due_date = models.DateField(verbose_name=_("Fecha de vencimiento"))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Estado")
    )
    description = models.TextField(blank=True, verbose_name=_("Descripción"))
    notes = models.TextField(blank=True, verbose_name=_("Notas"))
    pay_date = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Fecha de pago"))

    class Meta:
        verbose_name = _("Debt")
        verbose_name_plural = _("Debts")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.name} - ${self.pending_amount}"

    @property
    def pending_amount(self):
        return self.total_amount - self.paid_amount

    def pay(self, amount):
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        if amount > self.pending_amount:
            raise ValueError("El monto no puede ser mayor al pendiente")

        self.paid_amount += Decimal(str(amount))
        if self.paid_amount >= self.total_amount:
            self.status = 'paid'
            self.pay_date = datetime.now(timezone.utc)
        self.save()
