"""
Django settings for swissrugbystats project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'swissrugbystats')

# Import email settings in the form of
'''
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_PORT = 587
'''
# from settings_email import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6roh3)=1cp7vexm5^jbucmhwtif(p=f2j879vghfqrjm6z4qlb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['api.swissrugbystats.ch']


# Application definition

INSTALLED_APPS = (
    'django_admin_conf_vars',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'swissrugbystats.core',
    'swissrugbystats.coach',
    'swissrugbystats.crawler',
    'simple_history',
    'crispy_forms'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

ROOT_URLCONF = 'swissrugbystats.urls'

WSGI_APPLICATION = 'swissrugbystats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'de-ch'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, "static")


# Media files (Files uploaded by user)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

# CORS (Cross Origin Resource Sharing)
# documentation: https://github.com/ottoyiu/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True

# Django Rest Framework
# check http://www.django-rest-framework.org/api-guide/permissions/ for documentation about permissions
REST_FRAMEWORK = {
    # only helpful if you want to paginate in the frontend as well
    # 'PAGINATE_BY': 20,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

# JWT
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(seconds=1200),

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

# choose the user model
#AUTH_USER_MODEL = 'swissrugby.MyUser'
AUTH_USER_MODEL = 'auth.User'

# Django Resized
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True

# comment out following line for initial db migration
VARS_MODULE_PATH = 'swissrugbystats.my_conf_vars'