from django.core.paginator import Paginator


def update_stock(model, DebtItem):
    if not model.pk:
        # Si es una nueva instancia, reducir stock
        model.product.add_sale(model.quantity)
    else:
        # Si se está editando, obtener la instancia anterior
        old_instance = DebtItem.objects.get(pk=model.pk)

        # Restaurar stock del producto anterior si cambió
        if old_instance.product != model.product:
            model.product.add_sale(model.quantity)
        elif old_instance.quantity != model.quantity:
            # Si cambió la cantidad del mismo producto
            quantity_diff = model.quantity - old_instance.quantity
            if quantity_diff > 0:
                # Aumentó la cantidad, reducir más stock
                model.product.add_sale(quantity_diff)
            else:
                # Disminuyó la cantidad, restaurar stock
                model.product.stock += abs(quantity_diff)
                model.product.save()


def restaure_stock(model):
    # Restaurar stock al eliminar el item
    model.product.stock += model.quantity
    model.product.save()


def get_paginator(request, model, name, page_size=12):
    # Paginación
    paginator = Paginator(model, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return {
        name: page_obj,
        'page_obj': page_obj,
    }
