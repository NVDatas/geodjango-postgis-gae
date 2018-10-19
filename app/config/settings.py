# -*- coding: utf-8 -*-

import ctypes
import os

import environ
from os.path import abspath, dirname, join, normpath, isfile

from util import google_metadata

SITE_ROOT = dirname(dirname(abspath(__file__)))

env = environ.Env()

if os.getenv('GAE_INSTANCE'):
    attributes = google_metadata.get_project_attributes()
    for key, value in attributes.items():
        print('key: ', key, 'value: ', value)
        env.ENVIRON.setdefault(key, value)

    if os.getenv('GAE_ENV') == 'standard':
        os.environ.setdefault('GDAL_DATA', join(dirname(SITE_ROOT), 'usr/share/gdal'))
        ctypes.cdll.LoadLibrary(join(dirname(SITE_ROOT), 'usr/lib/libproj.so.13.1.1'))
        ctypes.cdll.LoadLibrary(join(dirname(SITE_ROOT), 'usr/lib/libgeos-3.6.3.so'))
        GEOS_LIBRARY_PATH = join(dirname(SITE_ROOT), 'usr/lib/libgeos_c.so.1.10.3')
        GDAL_LIBRARY_PATH = join(dirname(SITE_ROOT), 'usr/lib/libgdal.so')
else:
    env_file = join(dirname(SITE_ROOT), 'env/development/.env')
    if isfile(env_file):
        environ.Env.read_env(env_file=env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b=r$iq#q5wh@7vicmcp5neg=7#3*4(cb^j-kjz)_8vbusy+aa&'

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
DEBUG = env("DJANGO_DEBUG", cast=bool, default=False)
VERBOSE = env("DJANGO_VERBOSE", cast=bool, default=False)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Application definition
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
)
THIRD_PARTY_APPS = (
    'rest_framework',  # djangorestframework
    'rest_framework.authtoken',
    'rest_framework_gis',  # djangorestframework-gis
    'drf_yasg',  # drf-yasg
    'django_filters',
)
LOCAL_APPS = (
    # Apps specific for this project go here.
    'geo_japan',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            normpath(join(SITE_ROOT, 'templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# CACHING
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': env.cache('DJANGO_CACHES_DEFAULT_URL', 'locmemcache://'),
}

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': env('DJANGO_DATABASE_ENGINE'),
        'USER': env('DJANGO_DATABASE_USER'),
        'PASSWORD': env('DJANGO_DATABASE_PASSWORD'),
        'HOST': env('DJANGO_DATABASE_HOST'),
        'PORT': env('DJANGO_DATABASE_PORT'),
        'NAME': env('DJANGO_DATABASE_NAME'),
        'ATOMIC_REQUESTS': True,
    }
}

# e-mail
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("DJANGO_EMAIL_HOST", default="")
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env("DJANGO_EMAIL_PORT", cast=int, default="")
EMAIL_USE_TLS = env("DJANGO_EMAIL_USE_TLS", cast=bool, default=False)

# SESSIONS
# https://docs.djangoproject.com/en/dev/topics/http/sessions/
SESSION_ENGINE = env('DJANGO_SESSION_ENGINE', default='django.contrib.sessions.backends.db')

# MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT', default=normpath(join(dirname(SITE_ROOT), 'media')))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = env('DJANGO_STATIC_URL', default='/static/')
STATIC_ROOT = env('DJANGO_STATIC_ROOT', default=normpath(join(dirname(SITE_ROOT), 'static')))

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Host
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]


# django-debug-toolbar
if DEBUG and env("DJANGO_SHOW_DEBUG_TOOLBAR", cast=bool, default=False):
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }

# django-cors-middleware
CORS_ORIGIN_ALLOW_ALL = True

# djangorestframework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_jsonp.renderers.JSONPRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '10000/day'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'UNICODE_JSON': True,
    'COMPACT_JSON': False,
}

# drf-yasg
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.ReferencingSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    ],
}


# django_filters
def FILTERS_VERBOSE_LOOKUPS():
    from django_filters.conf import DEFAULTS

    verbose_lookups = DEFAULTS['VERBOSE_LOOKUPS'].copy()
    verbose_lookups.update({
        'gt': 'より大きい',
        'gte': '以上',
        'lt': 'より小さい',
        'lte': '以下',
    })
    return verbose_lookups


# Logging
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO' if DEBUG is False else 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'level': 'WARNING' if DEBUG is False else 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'WARNING' if VERBOSE is False else 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'geo_japan': {
            'level': 'INFO' if DEBUG is False else 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}
