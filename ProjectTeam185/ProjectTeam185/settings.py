"""
Django settings for ProjectTeam185 project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!d#+-)#(w4$i9351&g9w%k%!=zq14z5r4ac@q1j&5cdfvng3z@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Set this to True to avoid transmitting the session cookie over HTTP accidentally.
# SESSION_COOKIE_SECURE = True

# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
# CSRF_COOKIE_SECURE = True

# Using an HttpOnly CSRF cookie makes it more difficult for cross-site scripting attacks to steal the CSRF token.
# CSRF_COOKIE_HTTPONLY = True

# X_FRAME_OPTIONS = 'DENY'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'resuMe'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ProjectTeam185.urls'

WSGI_APPLICATION = 'ProjectTeam185.wsgi.application'

LOGIN_URL = '/resuMe/login'

LOGIN_REDIRECT_URL = '/'

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



# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# MEDIA_ROOT = 'resuMe/static/img'
MEDIA_ROOT = os.path.join(BASE_DIR,'resuMe/static/img')

MEDIA_URL = '/media/'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# To enable real email sending
EMAIL_USE_TLS=True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "muhuali3303@gmail.com"
EMAIL_HOST_PASSWORD = 'KUGEWUKANG'
EMAIL_PORT = 587

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = './static/'
