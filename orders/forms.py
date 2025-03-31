from django import forms
from .models import Order, Product, OrderItem


class OrderItemForm(forms.ModelForm):
    """
    Форма для добавления блюда с выбором количества.
    """
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(status="available"),  # Только доступные блюда
        empty_label="Выберите блюдо",
        label="Блюдо"
    )
    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


# Формсет для нескольких позиций в заказе
OrderItemFormSet = forms.inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    extra=0, can_delete=True
)


class OrderForm(forms.ModelForm):
    """
    Форма заказа, позволяющая выбрать блюда и их количество.
    """

    class Meta:
        model = Order
        fields = ['table_number', 'status']
