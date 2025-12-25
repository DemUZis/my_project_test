# Архитектурный план: Система управления салоном красоты "Время стиля"

## Обзор

Создание веб-приложения для управления салоном красоты с тремя основными ролями: клиенты, мастера и администраторы. Приложение будет включать в себя функции записи на услуги, управления персоналом, отслеживания отзывов и статистики.

## Стек технологий

- FastAPI (веб-фреймворк)
- SQLAlchemy (ORM)
- Alembic (миграции базы данных)
- SQLite (база данных)
- Jinja2 (шаблоны)
- HTML/CSS/JavaScript (фронтенд)
- Pydantic (валидация данных)

## Структура базы данных

### Таблицы

1. **Пользователи (Users)**
   - id (PK)
   - username
   - email
   - password_hash
   - role (client, master, admin)
   - created_at
   - updated_at

2. **Мастера (Masters)**
   - id (PK)
   - user_id (FK)
   - name
   - specialization
   - bio
   - created_at
   - updated_at

3. **Услуги (Services)**
   - id (PK)
   - name
   - description
   - duration (в минутах)
   - price
   - created_at
   - updated_at

4. **Сеансы (Sessions)**
   - id (PK)
   - master_id (FK)
   - service_id (FK)
   - date
   - start_time
   - end_time
   - is_available (булевое значение)
   - created_at
   - updated_at

5. **Записи (Appointments)**
   - id (PK)
   - client_id (FK)
   - session_id (FK)
   - status (booked, completed, cancelled)
   - created_at
   - updated_at

6. **Отзывы (Reviews)**
   - id (PK)
   - client_id (FK)
   - master_id (FK)
   - appointment_id (FK)
   - rating (1-5)
   - comment
   - created_at
   - updated_at

7. **Смены (Shifts)**
   - id (PK)
   - master_id (FK)
   - date
   - start_time
   - end_time
   - created_at
   - updated_at

## API Endpoints

### Аутентификация
- POST /auth/register
- POST /auth/login
- POST /auth/logout

### Клиенты
- GET /clients/profile
- GET /services (просмотр услуг)
- GET /masters (просмотр мастеров)
- GET /sessions/available (доступные сеансы)
- POST /appointments/book (запись на сеанс)
- GET /appointments/my (мои записи)
- POST /reviews (оставить отзыв)

### Мастера
- GET /masters/profile
- GET /masters/schedule
- GET /masters/appointments
- PUT /sessions/update-availability

### Администраторы
- GET /admin/dashboard
- POST /admin/services
- PUT /admin/services/{id}
- DELETE /admin/services/{id}
- GET /admin/services
- POST /admin/masters
- PUT /admin/masters/{id}
- DELETE /admin/masters/{id}
- GET /admin/masters
- GET /admin/appointments
- GET /admin/statistics
- GET /admin/revenue

## Веб-интерфейс

### Страницы

1. **Главная страница**
   - Приветствие
   - Описание салона
   - Популярные услуги

2. **Страница услуг**
   - Список всех услуг
   - Детали услуг

3. **Страница мастеров**
   - Список всех мастеров
   - Детали мастеров

4. **Страница записи**
   - Выбор услуги
   - Выбор мастера
   - Выбор времени

5. **Личный кабинет клиента**
   - Мои записи
   - История посещений
   - Оставить отзыв

6. **Личный кабинет мастера**
   - Мое расписание
   - Мои клиенты
   - Статус сеансов

7. **Панель администратора**
   - Управление услугами
   - Управление персоналом
   - Статистика и аналитика
   - Отчеты

## Визуальный дизайн

- Цветовая схема: синие тона
- Современный, чистый дизайн
- Адаптивный интерфейс

## Безопасность

- Хеширование паролей (bcrypt)
- JWT токены для аутентификации
- Валидация входных данных
- Защита от SQL-инъекций через ORM

## Масштабируемость

- Четкая архитектура с разделением на слои (API, сервисы, репозитории, модели)
- Использование зависимостей FastAPI
- Поддержка асинхронности