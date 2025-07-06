# 📦 Hotel Booking Project

Простое API для управления номерами отелей и бронированиями, написанное на **Python + Django + DRF** с использованием **PostgreSQL** и обёрткой в Docker.

---

## 🔧 **Технологии**

* Python 3.12
* Django 5.2
* Django REST Framework
* PostgreSQL 17.5
* Docker + docker-compose
* Poetry
* Pytest

---

## 🚀 **Запуск проекта локально**

### 1. **Клонируйте репозиторий**

```bash
git clone https://github.com/yourusername/hotel-booking-project.git
cd hotel-booking-project
```

---

### 2. **Создайте .env на основе .env.example**

```bash
cp .env.example .env
```

Заполните `SECRET_KEY` и при необходимости другие переменные.

---

### 3. **Соберите и запустите проект через Docker Compose**

```bash
docker-compose up --build
```

🔍 **API будет доступно на**: [http://localhost:8000](http://localhost:8000)

---

### 4. **Примените миграции**

```bash
docker-compose exec web python manage.py migrate
```
---

## 🗄 **ENV переменные**

| Переменная   | Описание           | Пример                  |
| ------------ | ------------------ | ----------------------- |
| DB\_NAME     | Имя БД             | hotel\_booking          |
| DB\_USER     | Пользователь БД    | postgres                |
| DB\_PASSWORD | Пароль БД          | postgres                |
| DB\_HOST     | Хост БД            | db                      |
| DB\_PORT     | Порт БД            | 5432                    |
| SECRET\_KEY  | Django SECRET\_KEY | your\_secret\_key\_here |
| DEBUG        | Включение debug    | True                    |

---

## 🧪 **Тесты**

Для запуска тестов:

```bash
pytest --cov
```

---

## 📫 **Примеры curl запросов**

### ➕ Создание комнаты

```bash
curl -X POST http://localhost:8000/rooms/ \
-H "Content-Type: application/json" \
-d '{"description": "Тестовый номер", "price": 1500}'
```

🖥️ **Response:**

```json
{
  "room_id": 1
}
```

---

### 📋 Получение списка комнат

```bash
curl http://localhost:8000/rooms/
```

🖥️ **Response:**

```json
[
  {
    "id": 1,
    "description": "Тестовый номер",
    "price": "1500.00",
    "created_at": "2025-07-01T12:00:00Z"
  }
]
```

---

### ➕ Создание бронирования

```bash
curl -X POST http://localhost:8000/bookings/ \
-H "Content-Type: application/json" \
-d '{"room": 1, "date_start": "2025-07-10", "date_end": "2025-07-12"}'
```

🖥️ **Response:**

```json
{
  "booking_id": "uuid"
}
```

---

### 📋 Получение списка броней по комнате

```bash
curl http://localhost:8000/bookings/?room_id=1
```

🖥️ **Response:**

```json
[
  {
    "id": "uuid",
    "date_start": "2025-07-10",
    "date_end": "2025-07-12"
  }
]
```

---

### ❌ Удаление комнаты

```bash
curl -X DELETE http://localhost:8000/rooms/1/
```

🖥️ **Response:**

```json
{
  "status": "Room 1 deleted"
}
```

---

### ❌ Удаление брони

```bash
curl -X DELETE http://localhost:8000/bookings/uuid/
```

🖥️ **Response:**

```json
{
  "status": "Booking uuid deleted"
}
```

---
