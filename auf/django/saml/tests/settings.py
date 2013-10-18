# -*- coding: utf-8 -*-

import os


USE_I18N = False

SECRET_KEY = 'secret'

ROOT_URLCONF = 'auf.django.saml.tests.urls'

DATABASES = {'default':
            {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:', }}

INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.admin',
                  'auf.django.saml', )


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auf.django.saml.middleware.SPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    )

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
    )
