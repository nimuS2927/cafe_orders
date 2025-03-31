from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Обновить статус заказа"""
        order = self.get_object()
        order.status = request.data.get('status', order.status)
        order.save()
        return Response({'status': order.status})

    @action(detail=True, methods=['post'])
    def recalculate_total(self, request, pk=None):
        """Пересчитать стоимость заказа"""
        order = self.get_object()
        order.calculate_total_price()
        return Response({'total_price': order.total_price})
