from django.db import models


class Product(models.Model):
    """
    Модель продукта (блюда) в кафе.
    """
    STATUS_CHOICES = [
        ('available', 'Доступно'),
        ('unavailable', 'Недоступно'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='available', verbose_name="Статус")

    def __str__(self):
        return f"{self.name} - {self.price}₽ ({self.get_status_display()})"


class Order(models.Model):
    """
    Модель заказа, содержащая номер стола, список блюд, общую стоимость и статус.
    """
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    id = models.AutoField(primary_key=True)
    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    items = models.ManyToManyField(Product, through='OrderItem', verbose_name="Список блюд")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость", default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    def calculate_total_price(self):
        """
        Пересчитывает общую стоимость заказа на основе товаров и их количества.
        """
        self.total_price = sum(item.product.price * item.quantity for item in self.order_items.all())
        self.save()

    def __str__(self):
        return f"Заказ {self.id} (Стол {self.table_number}) - {self.get_status_display()}"


class OrderItem(models.Model):
    """
    Промежуточная модель для связи "Многие ко многим" между Order и Product, добавляя поле "quantity".
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} x{self.quantity} в заказе {self.order.id}"
