"""Test settings and globals """

from __future__ import absolute_import

from .base import *

# DATABASE CONFIGURATION ------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# https://docs.djangoproject.com/en/1.10/topics/testing/overview/#the-test-database

# `On PostgreSQL, USER will also need read access to the built-in postgres
# database`

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pychan',
        'USER': 'moot',
        'PASSWORD': 'pychan',
        'HOST': 'localhost',
        'PORT': '',
    }
}
# END DATABASE CONFIGURATION --------------------------------------------------
