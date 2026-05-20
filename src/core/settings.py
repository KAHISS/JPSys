import os
import environ
from pathlib import Path
from django.contrib.messages import constants

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='django-insecure-substitua-isso-no-env')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

AUTH_USER_MODEL = 'users.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'apps.inventory',
    'apps.users',
    'apps.promoters',
    'apps.sales',
    'apps.catalog'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'base_templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3')
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'pt-br'  # Mudei para português, já que estamos aqui
TIME_ZONE = 'America/Sao_Paulo'  # Ajustado para o seu fuso

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'  # Recomendado adicionar para produção

STATICFILES_DIRS = [
    BASE_DIR / 'base_statics',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Recomendado adicionar para produção

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    constants.DEBUG: 'message-debug',
    constants.INFO: 'bg-blue-50 text-blue-800 border-blue-500',
    constants.SUCCESS: 'bg-green-50 text-green-800 border-green-500',
    constants.WARNING: 'bg-yellow-50 text-yellow-800 border-yellow-500',
    constants.ERROR: 'bg-red-50 text-red-800 border-red-500',
}

CSRF_TRUSTED_ORIGINS = [
    'https://atacadinhocristao.cloud',
    'https://www.atacadinhocristao.cloud',
    'http://localhost',
    'http://127.0.0.1',
]
