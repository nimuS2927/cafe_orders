from rest_framework import serializers
from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'status']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='order_items', required=False)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        order.calculate_total_price()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items', [])
        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Обновление или создание OrderItem
        instance.order_items.all().delete()  # Очистка старых позиций
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)

        instance.calculate_total_price()
        return instance
