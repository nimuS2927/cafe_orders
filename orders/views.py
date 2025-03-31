from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet


class OrderListView(ListView):
    """Список всех заказов"""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    queryset = Order.objects.prefetch_related('order_items__product')


class OrderCreateView(CreateView):
    """Создание нового заказа"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        """Добавляем formset для позиций заказа"""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
        else:
            context['formset'] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        """Сохраняем заказ и блюда"""
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            # Сохраняем заказ
            order = form.save(commit=False)
            order.save()
            # Привязываем блюда к заказу
            formset.instance = order
            # Сохраняем все блюда
            formset.save()
            # Пересчитываем общую стоимость заказа
            order.calculate_total_price()
            # Сохраняем заказ с обновленной стоимостью
            order.save()
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form))


class OrderUpdateView(UpdateView):
    """Редактирование заказа"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        """Добавляем formset для редактирования позиций заказа"""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """Сохраняем изменения заказа и блюда"""
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.instance = order
            formset.save()
            order.calculate_total_price()
            order.save()
            return redirect(self.success_url)
        else:
            print("Form is invalid:", form.errors)
            print("Formset is invalid:", formset.errors)
        return self.render_to_response(self.get_context_data(form=form))


class OrderDeleteView(DeleteView):
    """Удаление заказа"""
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')
