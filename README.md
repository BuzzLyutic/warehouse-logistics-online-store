<div align="center">

# Warehouse & Logistics Management System

### Микросервисная система управления складом и логистикой для интернет-магазина

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12+-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)](https://www.rabbitmq.com/)

[Возможности](#-возможности) • [Архитектура](#-архитектура) • [Установка](#-установка) • [API](#-api)

</div>

---

## 📋 О проекте

Система управления складом и логистикой, построенная на микросервисной архитектуре. Автоматизирует процессы инвентаризации, обработки заказов и отслеживания отгрузок для интернет-магазинов.

---

## ✨ Возможности

### 🏢 Для сотрудников склада
- 📊 Отслеживание уровня запасов в реальном времени
- 📥 Управление приходом/расходом товара
- 🏭 Работа с несколькими складами
- 📦 Автоматическая комплектация заказов

### 🛒 Для покупателей
- ✅ Создание заказов на доставку
- 🔍 Отслеживание статуса заказа
- 📱 Уведомления об изменении статуса

### 👨‍💼 Для администраторов
- 🔐 Управление пользователями и ролями
- 🛡️ Безопасная аутентификация (JWT)
- 📈 Аналитика по складу и заказам

---

## 🏗 Архитектура

### Микросервисная архитектура

<img width="974" height="906" alt="image" src="https://github.com/user-attachments/assets/0f8f5270-6d9a-4ed4-b093-e49edff4abf6" />

### Взаимодействие между компонентами

<img width="974" height="619" alt="image" src="https://github.com/user-attachments/assets/daaf58fa-2954-49d5-bba5-c6c609f8402c" />

### Определение контрактов между компонентами системы

<img width="613" height="662" alt="image" src="https://github.com/user-attachments/assets/d0b720f4-9219-4731-9898-cfa6a487fb7b" />

### Схема физической инфраструктуры

<img width="974" height="546" alt="image" src="https://github.com/user-attachments/assets/4e1b187b-1c50-48e4-b1b8-55124683e713" />

---

## 🛠 Технологический стек

### Backend
| Компонент | Технология | Назначение |
|-----------|-----------|-----------|
| Framework | **Django 4.2+** | REST API для каждого микросервиса |
| Databases | **PostgreSQL** | Auth, Inventory, Order |
|           | **MongoDB** | Shipment (документоориентированное хранение) |
| Message Queue | **RabbitMQ** | Асинхронное взаимодействие между сервисами |
| Task Queue | **Celery** | Фоновые задачи (уведомления, отчеты) |
| API Gateway | **NGINX** | Маршрутизация запросов, load balancing |

### Frontend
```
React 18 | React Router | Axios | Tailwind CSS
```

### DevOps
```
Docker | Docker Compose | Gunicorn
```

### Паттерны
- **MVC (MTV)** — в каждом Django сервисе
- **Repository Pattern** — абстракция доступа к данным
- **API Gateway** — единая точка входа
- **Event-Driven** — через RabbitMQ

---

## Установка

### Предварительные требования

- Docker 24+
- Docker Compose 2.20+

### Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/yourusername/warehouse-logistics.git
cd warehouse-logistics

# 2. Запустить все сервисы
docker-compose up --build

```

---

## 📡 API

### Скоро...

---

## 🧪 Тестирование

### Скоро...

---

## 🔒 Безопасность

- ✅ **JWT аутентификация** (access + refresh tokens)
- ✅ **RBAC** (Role-Based Access Control)
- ✅ **CORS** настройки
- ✅ **Rate limiting** через NGINX
- ✅ **Security headers** (CSP, X-Frame-Options, etc.)

---

## 🐳 Docker Compose

### Команды

```bash
# Запустить
docker-compose up

# Пересобрать
docker-compose up --build

# Остановить
docker-compose down

# Логи конкретного сервиса
docker-compose logs -f order-service

# Выполнить команду в контейнере
docker-compose exec order-service python manage.py migrate
```

---

## 📊 Мониторинг

### RabbitMQ Management

```
http://localhost:15672
Login: guest / guest
```

### Логи

```bash
# Все сервисы
docker-compose logs -f

# Только ошибки
docker-compose logs -f | grep ERROR
```

---

## 🤝 Contributing

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

<div align="center">

**⭐ Поставьте звезду, если проект полезен!**

Made with 📦 for e-commerce logistics

</div>

---
