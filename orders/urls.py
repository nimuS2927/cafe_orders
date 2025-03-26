from django.urls import path
from .views import order_list, order_create, order_update, order_delete

urlpatterns = [
    path('', order_list, name='order_list'),
    path('new/', order_create, name='order_create'),
    path('<int:order_id>/edit/', order_update, name='order_update'),
    path('<int:order_id>/delete/', order_delete, name='order_delete'),
]
