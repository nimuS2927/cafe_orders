from django.db import models


class Product(models.Model):
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
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    id = models.AutoField(primary_key=True)
    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    items = models.ManyToManyField(Product, related_name="orders", verbose_name="Список блюд")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость", default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    def save(self, *args, **kwargs):
        # Пересчитываем сумму перед сохранением
        self.total_price = sum(product.price for product in self.items.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.id} (Стол {self.table_number}) - {self.get_status_display()}"
