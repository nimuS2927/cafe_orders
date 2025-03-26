from django import forms
from .models import Order, Product, OrderItem


class OrderItemForm(forms.ModelForm):
    """
    Форма для добавления блюда с выбором количества.
    """
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderForm(forms.ModelForm):
    """
    Форма заказа, позволяющая выбрать блюда и их количество.
    """
    table_number = forms.IntegerField(label="Номер стола")
    products = forms.ModelChoiceField(
        queryset=Product.objects.filter(status='available'),
        label="Выберите блюдо"
    )
    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")

    class Meta:
        model = Order
        fields = ['table_number', 'status']

    def save(self, commit=True):
        """
        Сохранение заказа с учетом выбора количества блюд.
        """
        order = super().save(commit=False)
        if commit:
            order.save()
            OrderItem.objects.create(order=order, product=self.cleaned_data['products'],
                                     quantity=self.cleaned_data['quantity'])
            order.calculate_total_price()
        return order
