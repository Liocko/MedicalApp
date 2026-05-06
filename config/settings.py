"""
Настройки Django проекта в соответствии с принципами 12 Factor App
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Функция для получения переменных окружения с проверкой
def get_env_variable(var_name, default=None):
    """Получает переменную окружения или выбрасывает ошибку если не найдена"""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = f"Установите переменную окружения {var_name}"
            raise ImproperlyConfigured(error_msg)

# Базовые настройки
SECRET_KEY = get_env_variable('SECRET_KEY')
DEBUG = get_env_variable('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Приложения
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "phonenumber_field",
    "social_django",

    "core",
    "patients",
    "records",
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.yandex.YandexOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# База данных
DATABASE_URL = get_env_variable('DATABASE_URL', 'sqlite:///db.sqlite3')
if DATABASE_URL.startswith('postgres://'):
    # Настройка PostgreSQL
    import urllib.parse
    
    parsed = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path[1:],
            'USER': parsed.username,
            'PASSWORD': parsed.password,
            'HOST': parsed.hostname,
            'PORT': parsed.port,
        }
    }
else:
    # Настройка SQLite по умолчанию
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Проверка на необходимые переменные окружения
if not SECRET_KEY or SECRET_KEY == 'unsafe-dev-key':
    raise ImproperlyConfigured("SECRET_KEY должен быть установлен в переменных окружения")

# Парольные валидаторы
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Интернационализация
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = get_env_variable('TIME_ZONE', 'Europe/Moscow')
USE_I18N = True
USE_TZ = get_env_variable('USE_TZ', 'True').lower() == 'true'

# Статические файлы
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Поле по умолчанию
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Авторизация
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Телефонные номера
PHONENUMBER_DEFAULT_REGION = 'RU'

# Яндекс OAuth
SOCIAL_AUTH_YANDEX_OAUTH2_KEY = get_env_variable('YANDEX_CLIENT_ID', '')
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = get_env_variable('YANDEX_CLIENT_SECRET', '')
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

