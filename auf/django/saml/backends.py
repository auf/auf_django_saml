# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import User
from django.contrib.auth.backends import RemoteUserBackend, ModelBackend
from auf.django.saml import settings


logger = logging.getLogger('SAML')


class _BackendMixin:

    def clean_username(self, username):
        info = u"username original : %s" % username
        clean_username = username.replace('@auf.org', '')
        info += u"\nusername clean : %s" % clean_username
        logger.info(info)
        return clean_username


class FakeSPBackend(_BackendMixin, ModelBackend,):
    """
    On autentifie uniquement sur le username
    """

    def authenticate(self, username=None, password=None):
        username = self.clean_username(username)
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


class RealSPBackend(_BackendMixin, RemoteUserBackend):
    """
    Backend reposant sur le id.auf.org
    """
    create_unknown_user = settings.SAML_AUTO_CREATION


if settings.SAML_AUTH:
    _SPBackend = RealSPBackend
else:
    _SPBackend = FakeSPBackend


class SPBackend(_SPBackend):
    """
    Backend selon la conf
    """

    def authenticate(self, *args, **kwargs):
        info = u"%s" % __name__
        for k, v in kwargs.items():
            if k == 'password':
                v = '****'
            info += "\n* %s : %s" % (k, v)
        logger.info(info)

        user = super(SPBackend, self).authenticate(*args, **kwargs)
        info = u"Django user authentifié : %s" % user
        logger.info(info)
        return user
