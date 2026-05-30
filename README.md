# TeamFinder

Дипломный проект для Яндекс практикум.

Реализован **Вариант 1**: избранное и фильтрация участников.

## Технологии

- Python 3.11 / Django 5.2
- PostgreSQL
- Pillow — генерация аватарок

## Как запустить

### Через Docker (рекомендую)

```bash
cp .env.example .env
docker-compose up --build
```

Откройте http://localhost:8000 — всё готово.

### Локально

Понадобятся Python 3.11+ и запущенный PostgreSQL.

```bash
pip install -r requirements.txt

cp .env.example .env
# Заполните .env своими данными (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)

python manage.py migrate
python manage.py createsuperuser

# Загрузить тестовых пользователей и проекты
python manage.py create_test_data

python manage.py runserver
```

### Тестовые аккаунты

| Email | Пароль |
|-------|--------|
| alice@example.com | testpass123 |
| bob@example.com | testpass123 |
| carol@example.com | testpass123 |

## Структура проекта

```
config/     — настройки Django
users/      — всё, что касается пользователей: модели, формы, вьюхи
projects/   — проекты и связанная логика
templates/  — шаблоны
static/     — стили и скрипты
```

## Страницы и URL-адреса

| URL | Что здесь |
|-----|-----------|
| `/` | Редирект на главную |
| `/projects/list/` | Список проектов (12 на страницу) |
| `/projects/<id>/` | Карточка проекта |
| `/projects/create-project/` | Создать проект |
| `/projects/<id>/edit/` | Редактировать проект |
| `/projects/<id>/complete/` | Завершить проект (POST → JSON) |
| `/projects/<id>/toggle-favorite/` | Добавить/убрать из избранного (POST → JSON) |
| `/projects/<id>/toggle-participate/` | Вступить/выйти из проекта (POST → JSON) |
| `/projects/favorites/` | Мои избранные проекты |
| `/users/list/` | Список участников |
| `/users/<id>/` | Профиль пользователя |
| `/users/register/` | Регистрация |
| `/users/login/` | Вход |
| `/users/logout/` | Выход |
| `/users/edit-profile/` | Редактирование профиля |
| `/users/change-password/` | Смена пароля |

## Особенности

**Аутентификация по email** — стандартный Django заменён на кастомный `EmailBackend`, логин по email + пароль.

**Аватарки** — генерируются автоматически при регистрации: первая буква имени на цветном фоне (Pillow). Пользователь может заменить на своё фото.

**Телефон** — принимается в двух форматах (`8XXXXXXXXXX` или `+7XXXXXXXXXX`), нормализуется к `+7...` перед сохранением. Уникальность проверяется с учётом обоих форматов.

**Фильтры участников** — доступны только авторизованным пользователям:
- авторы проектов из моего избранного
- авторы проектов, в которых я участвую
- пользователи, которым нравятся мои проекты
- участники моих проектов
