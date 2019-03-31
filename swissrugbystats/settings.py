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
BASE_URL = os.environ.get('BASE_URL', "http://api.swissrugbystats.ch")

# TODO: Email backend settings for allauth
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
if 'PROD' in os.environ and os.environ['PROD'] == 'True':
    DEBUG = False

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    DEBUG = True

# even in prod debug can be enabled
if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'True':
    DEBUG = True

ALLOWED_HOSTS = [
    'swissrugbystats.ch',
    'api.swissrugbystats.ch',
    'api3.swissrugbystats.ch',
    'localhost',
    'swissrugbystats-backend.herokuapp.com',
    'swissrugbystats-frontend.herokuapp.com'
]

# Application definition

INSTALLED_APPS = (
    # 'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # restframework
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'rest_framework_swagger',
    # auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'rest_auth',
    # swissrugbystats apps
    'swissrugbystats.core',
    'swissrugbystats.coach',
    'swissrugbystats.crawler',
    'simple_history',
    'crispy_forms'
)

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROOT_URLCONF = 'swissrugbystats.urls'

WSGI_APPLICATION = 'swissrugbystats.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if 'PROD' in os.environ and os.environ['PROD'] == 'True':
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config()
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

ROLLBAR = {
    'access_token': os.environ.get('ROLLBAR_ACCESS_TOKEN', ''),
    'environment': 'development' if DEBUG else 'production',
    'branch': 'master',
    'root': PROJECT_DIR,
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (Files uploaded by user)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'frontend/templates/')
        ],
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
        'rest_framework.authentication.TokenAuthentication',
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # 'rest_framework_social_oauth2.authentication.SocialAuthentication'
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

AUTHENTICATION_BACKENDS = (
    # Django
    'django.contrib.auth.backends.ModelBackend',

    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# choose the user model
AUTH_USER_MODEL = 'auth.User'

# Django Resized
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True

# custom global vars, can be overwritten by env
CURRENT_SEASON = os.environ.get('CURRENT_SEASON', 1)
COMPETITIONS_BASE_URL = os.environ.get("COMPETITIONS_BASE_URL", "http://www.suisserugby.com/competitions/")
ARCHIVE_BASE_URL = os.environ.get("ARCHIVE_BASE_URL", "http://www.suisserugby.com/competitions/archiv/")
FIXTURES_URL_ENDING = os.environ.get("FIXTURES_URL_ENDING", "/lt/fixtures.html")
RESULTS_URL_ENDING = os.environ.get("RESULTS_URL_ENDING", "/lt/results.html")
LEAGUE_URL_ENDING = os.environ.get("LEAGUE_URL_ENDING", ".html")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

SITE_ID = 1
