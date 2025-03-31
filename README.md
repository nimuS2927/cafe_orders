# Cafe Orders

## Описание проекта

**Cafe Orders** – это веб-приложение на Django для управления заказами в кафе. Позволяет пользователям просматривать меню, делать заказы и управлять статусами через API и административную панель.

## Функциональность
- Административная панель для управления меню и заказами
- REST API для работы с заказами и продуктами
- Поддержка документации API через Swagger и ReDoc
- Возможность пересчета стоимости заказа

## Установка

### 1. Клонирование репозитория
```sh
git clone https://github.com/nimuS2927/cafe_orders
cd cafe_orders
```

### 2. Создание виртуального окружения
```sh
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

### 3. Установка зависимостей
```sh
pip install -r requirements.txt
```

### 4. Применение миграций и создание администратора
```sh
python manage.py migrate
python manage.py createsuperuser  # Создание суперпользователя для админ-панели
```

### 5. Запуск сервера
```sh
python manage.py runserver
```
Приложение будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API документация
Swagger: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)  
ReDoc: [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

## API Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/orders/` | Получить список заказов |
| POST | `/api/orders/` | Создать заказ |
| GET | `/api/orders/{id}/` | Получить информацию о заказе |
| PATCH | `/api/orders/{id}/` | Обновить заказ |
| POST | `/api/orders/{id}/update_status/` | Изменить статус заказа |
| POST | `/api/orders/{id}/recalculate_total/` | Пересчитать стоимость заказа |
| GET | `/api/products/` | Получить список продуктов |
| POST | `/api/products/` | Добавить новый продукт |


## Контакты
Автор: **Сумин Иван**  
Email: sumin.ivan01@mail.ru

