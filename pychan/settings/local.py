"""Development settings and globals """

from .base import *


# CELERY CONFIGURATION --------------------------------------------------------
# http://docs.celeryproject.org/en/latest/configuration.html#broker-url
BROKER_URL = 'amqp://guest:guest@localhost//'

# https://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'rpc://'
# END CELERY CONFIGURATION ----------------------------------------------------


# DEBUG CONFIGURATION ---------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# END DEBUG CONFIGURATION -----------------------------------------------------


# APPS CONFIGURATION ----------------------------------------------------------

# Debug Toolbar
# http://django-debug-toolbar.readthedocs.io/en/latest/installation.html

# Django Extras
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html


INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ('127.0.0.1',)
# END APPS CONFIGURATION ------------------------------------------------------


# DATABASE CONFIGURATION ------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pychan',
    }
}
# END DATABASE CONFIGURATION --------------------------------------------------
