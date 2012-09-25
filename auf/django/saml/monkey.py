# -*- coding: utf-8 -*-

"""
Setup automatique de LOGIN_URL et LOGOUT_URL
si SAML_AUTO_AUTH_URLS est positionné à True
"""

import django
from django.conf import settings
import settings as saml_settings


if saml_settings.SAML_AUTO_AUTH_URLS:
    if saml_settings.SAML_AUTH:
        LOGIN_URL = '/mellon/login'
        LOGOUT_URL = '/logout'
    else:
        LOGIN_URL = '/sandbox/login'
        LOGOUT_URL = '/sandbox/logout'

    django.contrib.auth.REDIRECT_FIELD_NAME = saml_settings.SAML_REDIRECT_FIELD_NAME
    settings.LOGIN_URL = LOGIN_URL
    settings.LOGOUT_URL = LOGOUT_URL
