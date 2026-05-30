# TeamFinder

Платформа для поиска единомышленников на pet-проекты. **Вариант 1**: Избранное + фильтрация пользователей.

## Стек

- Django 5.2 (кастомная модель пользователя, авторизация по email)
- PostgreSQL
- Pillow (генерация аватарок)

## Запуск через Docker Compose

```bash
cp .env.example .env
docker-compose up --build
```

Приложение доступно на http://localhost:8000

## Запуск локально

### Требования
- Python 3.11+
- PostgreSQL

```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения
cp .env.example .env
# Отредактируйте .env: укажите DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

# Миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Создать тестовые данные (3 пользователя, 4 проекта)
python manage.py create_test_data

# Запустить сервер
python manage.py runserver
```

### Тестовые аккаунты

После `create_test_data`:

| Email | Пароль |
|-------|--------|
| alice@example.com | testpass123 |
| bob@example.com | testpass123 |
| carol@example.com | testpass123 |

## Структура

```
config/        — настройки Django
users/         — приложение пользователей (модель, формы, вьюхи)
projects/      — приложение проектов
templates/     — HTML-шаблоны
static/        — CSS, JS
```

## Реализованные URL

| URL | Описание |
|-----|----------|
| `/` | Редирект на список проектов |
| `/projects/list/` | Главная — список проектов (12 на странице) |
| `/projects/<id>/` | Страница проекта |
| `/projects/create-project/` | Создание проекта |
| `/projects/<id>/edit/` | Редактирование проекта |
| `/projects/<id>/complete/` | Завершить проект (POST, JSON) |
| `/projects/<id>/toggle-favorite/` | Избранное (POST, JSON) |
| `/projects/<id>/toggle-participate/` | Участие (POST, JSON) |
| `/projects/favorites/` | Список избранного |
| `/users/list/` | Список участников с фильтрами |
| `/users/<id>/` | Профиль пользователя |
| `/users/register/` | Регистрация |
| `/users/login/` | Вход |
| `/users/logout/` | Выход |
| `/users/edit-profile/` | Редактирование профиля |
| `/users/change-password/` | Смена пароля |

## Особенности реализации

- **Авторизация** — по email (кастомный `EmailBackend`)
- **Аватарки** — автогенерируются при создании пользователя (Pillow: буква имени на цветном фоне)
- **Телефон** — хранится в формате `+7XXXXXXXXXX`, принимает `8XXXXXXXXXX` или `+7XXXXXXXXXX`
- **Фильтры участников** (только для авторизованных): авторы избранных, авторы проектов где участвую, кому нравятся мои проекты, участники моих проектов
