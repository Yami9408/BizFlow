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

    stock = models.PositiveIntegerField(default=0, verbose_name=_("Stock"))
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
