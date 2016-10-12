"""Development settings and globals """

from .base import *


# CELERY CONFIGURATION --------------------------------------------------------
# http://docs.celeryproject.org/en/latest/configuration.html#broker-url
BROKER_URL = 'amqp://guest:guest@localhost//'

# https://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'rpc://'
# END CELERY CONFIGURATION ----------------------------------------------------

# DATABASE CONFIGURATION ------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pychan',
    }
}
# END DATABASE CONFIGURATION --------------------------------------------------
