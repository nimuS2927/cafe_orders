from django.urls import path
from .views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView


urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('new/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/edit/', OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
]
