from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm


def order_list(request):
    """
    Представление списка всех заказов.
    """
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_create(request):
    """
    Представление создания нового заказа.
    """
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})


def order_update(request, order_id):
    """
    Представление редактирования заказа.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form})


def order_delete(request, order_id):
    """
    Представление удаления заказа.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})
