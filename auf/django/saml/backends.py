# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import User
from django.contrib.auth.backends import RemoteUserBackend, ModelBackend
from auf.django.saml import settings


logger = logging.getLogger('SAML')


class _BackendMixin:

    def clean_username(self, username):
        logger.info(u"\nClean username")
        logger.info(u"==============")
        logger.info(u"username original : %s" % username)
        clean_username = username.replace('@auf.org', '')
        logger.info(u"username clean : %s" % clean_username)


class FakeSPBackend(ModelBackend, _BackendMixin):
    """
    On autentifie uniquement sur le username
    """

    def authenticate(self, username=None, password=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


class RealSPBackend(RemoteUserBackend, _BackendMixin):
    """
    Backend reposant sur le id.auf.org
    """
    create_unknown_user = getattr(settings, 'SAML_AUTO_CREATION', True)


if settings.SAML_AUTH:
    _SPBackend = RealSPBackend
else:
    _SPBackend = FakeSPBackend


class SPBackend(_SPBackend):
    """
    Backend selon la conf
    """

    def authenticate(self, **kwargs):
        logger.info(u"\nauth challenge")
        logger.info(u"==============")
        for k, v in kwargs.items():
            if k == 'password':
                v = '****'
            logger.info("* %s : %s" % (k, v))

        user = super(SPBackend, self).authenticate(**kwargs)
        logger.info(u"Django user authentifié : %s" % user)
        return user
