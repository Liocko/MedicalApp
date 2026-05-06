# MedicalApp

Веб-система учёта медицинских карт пациентов поликлиники.  
Выполнена в рамках курсового проекта по дисциплинам «АКСП» и «Backend-разработка».

## Стек технологий

| Категория | Выбор |
|---|---|
| Язык | Python 3.12 |
| Фреймворк | Django 5.2 + Django REST Framework 3.16 |
| База данных | PostgreSQL (prod), SQLite (dev) |
| Frontend | Django Templates + Bootstrap 5 + кастомный CSS |
| Аутентификация | Django Auth + Yandex OAuth2 |
| Контейнеризация | Docker + docker-compose |
| Тестирование | unittest + hypothesis (фаззинг) |

## Архитектура

Проект следует принципам [12 Factor App](https://12factor.net/):
- вся конфигурация — через переменные окружения
- поддержка SQLite (разработка) и PostgreSQL (прод) через `DATABASE_URL`

**Приложения Django:**
- `core/` — главная страница, профиль пользователя
- `patients/` — модели Patient и Doctor, CRUD-интерфейс
- `records/` — модели MedicalRecord и Report, фильтрация записей

**REST API** доступен по `/api/v1/` (требует авторизации):
- `GET/POST /api/v1/patients/`
- `GET/PUT/PATCH/DELETE /api/v1/patients/{id}/`
- `GET/POST /api/v1/doctors/`
- `GET/PUT/PATCH/DELETE /api/v1/doctors/{id}/`
- `GET/POST /api/v1/records/`
- `GET/PUT/PATCH/DELETE /api/v1/records/{id}/`
- `GET/POST /api/v1/reports/`

Все endpoints поддерживают поиск (`?search=`) и сортировку (`?ordering=`).

## Быстрый старт

```bash
git clone <repo-url>
cd MedicalApp
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # задайте SECRET_KEY
python manage.py migrate
python manage.py seed       # заполнить БД тестовыми данными
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

## Переменные окружения

| Переменная | Обязательная | По умолчанию |
|---|---|---|
| `SECRET_KEY` | Да | — |
| `DEBUG` | Нет | `False` |
| `ALLOWED_HOSTS` | Нет | `127.0.0.1,localhost` |
| `DATABASE_URL` | Нет | `sqlite:///db.sqlite3` |
| `YANDEX_CLIENT_ID` | Нет | `''` |
| `YANDEX_CLIENT_SECRET` | Нет | `''` |

Пример для PostgreSQL:
```
DATABASE_URL=postgres://user:password@localhost:5432/medicalapp
```

## Docker

```bash
docker-compose up
```

Для production используйте gunicorn (включён в requirements):
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Тесты

```bash
# Все тесты
python manage.py test

# Фаззинг-тесты (hypothesis)
python manage.py test patients.tests.test_fuzz

# По приложению
python manage.py test patients
python manage.py test records
```

Фаззинг-тесты генерируют случайные входные данные и проверяют, что API не возвращает 500. Каждый тест выполняет 20–30 примеров с произвольными текстами, датами и email-адресами.

## Аутентификация

- Форма входа: `/login/`
- Yandex OAuth2: `/login/` → «Войти через Яндекс»
- REST API: Session Auth или Basic Auth
- Browsable API: `/api/v1/`

## Структура проекта

```
MedicalApp/
├── config/          # настройки, корневой urls.py
├── core/            # главная страница, UserProfile
├── patients/        # Patient, Doctor + сериализаторы + API + фаззинг
├── records/         # MedicalRecord, Report + сериализаторы + API
├── templates/       # base.html, login, страницы
├── requirements.txt
├── docker-compose.yml
└── manage.py
```
