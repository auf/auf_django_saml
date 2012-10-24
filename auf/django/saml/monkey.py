# -*- coding: utf-8 -*-

"""
Setup automatique de LOGIN_URL et LOGOUT_URL
si SAML_AUTO_AUTH_URLS est positionné à True
"""

import logging

import django
from django.utils.functional import update_wrapper
from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as _

import settings as saml_settings


logger = logging.getLogger('SAML')


if saml_settings.SAML_AUTO_AUTH_URLS:
    logger.info(u"\nPatch Auth settings")
    logger.info(u"===================")
    if saml_settings.SAML_AUTH:
        LOGIN_URL = '/mellon/login'
        LOGOUT_URL = '/logout'
    else:
        LOGIN_URL = '/sandbox/login'
        LOGOUT_URL = '/sandbox/logout'
    logger.info(u"* LOGIN_URL: %s" % LOGIN_URL)
    logger.info(u"* LOGOUT_URL: %s" % LOGOUT_URL)
    logger.info(u"* REDIRECT_FIELD_NAME: %s" %
            saml_settings.SAML_REDIRECT_FIELD_NAME)

    django.contrib.auth.REDIRECT_FIELD_NAME = \
        saml_settings.SAML_REDIRECT_FIELD_NAME
    settings.LOGIN_URL = LOGIN_URL
    settings.LOGOUT_URL = LOGOUT_URL

from django.contrib.admin import site
original_admin_view = site.__class__.admin_view


def custom_admin_view(self, view, cacheable=False):
    """
    Sur la page d'index, si on on ne dispose pas des accès, ne pas
    demander de se logger car dans le cas de id.auf, on crée un loop
    car on peut être déjà loggé sur id.auf mais on ne dispose pas des
    droits d'accès à l'admin.
    Sinon, on conserve le comportement normal.
    """

    def inner(request, *args, **kwargs):
        """
        """
        if not self.has_permission(request):
            return HttpResponseForbidden(
                    _(u"Votre compte ne permet pas d'accéder à cette page"))
        return view(request, *args, **kwargs)

    if view.__name__ == 'index':
        return update_wrapper(inner, view)
    else:
        return original_admin_view(self, view, cacheable=False)

logger.info(u"\nPatch de la admin.site pour gérer le \
            login forcé de la page d'index")
site.__class__.admin_view = custom_admin_view
