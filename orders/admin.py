from django.contrib import admin
from .models import Order, Product, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Количество пустых полей для новых записей
    autocomplete_fields = ['product']  # Удобный поиск продуктов
    readonly_fields = ['subtotal']  # Отображаем стоимость позиции

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = "Сумма"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('table_number',)
    inlines = [OrderItemInline]
    readonly_fields = ['total_price']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'status')
    list_filter = ('status',)
    search_fields = ('name',)

