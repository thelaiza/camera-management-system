from pathlib import Path
import dj_database_url
import os
from datetime import timedelta
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*8opdxtya-$k)$c+-%djm@h3-$8i^krqmwyeo5azg2i42%&n-('

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1", "localhost"
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend.api',
    "rest_framework",
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'user-id',
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://uc1d7c33rol0ai:p2226f5565accc54c3e667709fb7fc30f6e6298b2015b52cbe2808466fba5e7f1@ca8lne8pi75f88.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/demu7u61dqmqeh',
        conn_max_age=600
    )
}

DATABASES['default']['TEST'] = {
    'MIRROR': 'default',
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
