"""Common settings and globals."""

from __future__ import absolute_import

from os.path import abspath, basename, dirname, join, normpath
from sys import path

import os

# Normally you should not import ANYTHING from Django directly into your
# settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get an environment variable or return an exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)


# CELERY CONFIGURATION --------------------------------------------------------
# https://docs.celeryproject.org/en/latest/configuration.html#celery-accept-content
CELERY_ACCEPT_CONTENT = ['json']

# https://docs.celeryproject.org/en/latest/configuration.html#celery-task-serializer
CELERY_TASK_SERIALIZER = 'json'

# https://docs.celeryproject.org/en/latest/configuration.html#celery-result-serializer
CELERY_RESULT_SERIALIZER = 'json'

# https://docs.celeryproject.org/en/latest/configuration.html#celery-imports
CELERY_IMPORTS = ('boards.tasks',)
# END CELERY CONFIGURATION ----------------------------------------------------


# PATH CONFIGURATION ----------------------------------------------------------
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
# END PATH CONFIGURATION ------------------------------------------------------


# DEBUG CONFIGURATION ---------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
# END DEBUG CONFIGURATION -----------------------------------------------------


# MANAGER CONFIGURATION -------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Jack Evans', 'jack@evans.gb.net'),
)

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# END MANAGER CONFIGURATION ---------------------------------------------------


# DATABASE CONFIGURATION ------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db.sqlite3'),
    }
}
# END DATABASE CONFIGURATION --------------------------------------------------


# CACHE CONFIGURATION ---------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
# END CACHE CONFIGURATION -----------------------------------------------------


# GENERAL CONFIGURATION -------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/London'

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-gb'

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# END GENERAL CONFIGURATION ---------------------------------------------------


# MEDIA CONFIGURATION ---------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
# END MEDIA CONFIGURATION -----------------------------------------------------


# STATIC FILE CONFIGURATION ---------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/dev/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# https://docs.djangoproject.com/en/dev/ref/settings/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# END STATIC FILE CONFIGURATION -----------------------------------------------


# SECRET CONFIGURATION --------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = get_env_variable('SECRET_KEY')

# END SECRET CONFIGURATION ----------------------------------------------------


# SITE CONFIGURATION ----------------------------------------------------------
# Hosts/domain names that are valid for this site
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
# END SITE CONFIGURATION -----------------------------------------------------


# TEMPLATE CONFIGURATION ------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
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
# END TEMPLATE CONFIGURATION -------------------------------------------------


# MIDDLEWARE CONFIGURATION ---------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# END MIDDLEWARE CONFIGURATION ------------------------------------------------


# URL CONFIGURATION ----------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'pychan.urls'
# END URL CONFIGURATION ------------------------------------------------------


# APP CONFIGURATION ----------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'widget_tweaks',
    'captcha',
    'boards.apps.BoardsConfig',
]

RECAPTCHA_PUBLIC_KEY = '6LdehgkUAAAAALe6Y9SEQmkAPWQcHGG6Kv0sqDnO'
RECAPTCHA_PRIVATE_KEY = '6LdehgkUAAAAAIEVMDp9nMuVjrWJJ6Qe3-9bVzK9'
NOCAPTCHA = True

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
# END APP CONFIGURATION -------------------------------------------------------


# WSGI CONFIGURATION -------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'pychan.wsgi.application'
# END WSGI CONFIGURATION ---------------------------------------------------


# AUTHENTICATION CONFIGURATION -----------------------------------------------
# https://docs.djangoproject.com/en/1.10/ref/settings/#logout-redirect-url
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = "boards.Poster"

# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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
# END AUTHENTICATION CONFIGURATION --------------------------------------------


