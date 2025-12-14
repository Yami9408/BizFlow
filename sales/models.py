from datetime import datetime, timezone
from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.translation import gettext as _
STATUS_PENDING = 'pending'
STATUS_PAID = 'paid'
STATUS_OVERDUE = 'overdue'

STATUS_CHOICES = [
    (STATUS_PENDING, _('Pendiente')),
    (STATUS_PAID, _('Pagada')),
    (STATUS_OVERDUE, _('Vencida')),
]


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
    created_at = models.DateTimeField(
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
    client_name = models.CharField(
        max_length=100,
        verbose_name=_("Nombre del cliente")
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        # validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Monto total"),
        blank=True, null=True
    )
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Monto pagado")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación")
    )
    due_date = models.DateField(
        verbose_name=_("Fecha de vencimiento"),
        null=True, blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name=_("Estado"),
        db_index=True
    )
    description = models.TextField(blank=True, verbose_name=_("Descripción"))
    notes = models.TextField(blank=True, verbose_name=_("Notas"))
    pay_date = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Fecha de pago")
    )

    class Meta:
        verbose_name = _("Debt")
        verbose_name_plural = _("Debts")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - ${self.pending_amount}"

    @property
    def pending_amount(self):
        return self.total_amount - self.paid_amount

    def pay(self, amount=None):
        if not amount:
            amount = self.pending_amount
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        if amount > self.pending_amount:
            raise ValueError("El monto no puede ser mayor al pendiente")

        self.paid_amount += Decimal(str(amount))
        if self.paid_amount >= self.total_amount:
            self.status = 'paid'
            self.pay_date = datetime.now(timezone.utc)
        self.save()

    def calculate_total(self):
        total = sum(item.subtotal for item in self.product_items.all())
        self.total_amount = total
        self.save()


class DebtItem(models.Model):
    debt = models.ForeignKey(
        Debts,
        on_delete=models.CASCADE,
        related_name='product_items',
        verbose_name=_("Deuda")
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name=_("Producto")
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_("Cantidad")
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Precio unitario"),
        blank=True
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Subtotal"),
        blank=True
    )

    class Meta:
        verbose_name = _("Debt Product")
        verbose_name_plural = _("Debt Products")

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.sale_price_mn
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)
