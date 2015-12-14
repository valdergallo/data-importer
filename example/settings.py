#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Django settings for example project.
import os
import sys

data_importer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(data_importer_path)
sys.path.append('.')


BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'example.sqlite',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASEDIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASEDIR, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cxq@*7xgd763hq5hy30bdcr2r%(m)()kk$$qj(rpa@3%_i!q+6'

ROOT_URLCONF = 'example.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'example.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

AUTH_USER_MODEL = 'auth.User'

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'example',
    'data_importer',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    }

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    # '--with-coverage',
    '--cover-html',
    '--cover-package=data_importer',
    '--cover-tests',
    '--cover-erase',
    ]

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/invest-messages'  # change this to a proper location
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


SOUTH_MIGRATION_MODULES = {
    'data_importer': 'data_importer.south_migrations',
}

MIGRATION_MODULES = {
    'data_importer': 'data_importer.django_migrations'
},
