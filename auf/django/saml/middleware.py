# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.middleware import RemoteUserMiddleware
from auf.django.saml import settings as saml_settings

logger = logging.getLogger('SAML')


class SPMiddleware(RemoteUserMiddleware):

    def process_request(self, request):
        """
        Log MELLON an REMOTE_USER
        """
        logger.info(u"\nProcess request")
        logger.info(u"===============")
        for k, v in request.META.items():
            if k.startswith('MELLON') or k is 'REMOTE_USER':
                logger.info('%s : %s' % (k, v))

        if not saml_settings.SAML_AUTH:
            return
        return super(SPMiddleware, self).process_request(request)


def configure_user(sender, request, user, *args, **kwargs):
    """
    Au login, on synchronise les infos du serveur d'identités
    avec le user local
    """
    if saml_settings.SAML_AUTH:
        logger.info(u"* synchro du user local avec les infos de id.auf")
        meta = request.META
        user.email = meta['MELLON_mail']
        user.first_name = meta['MELLON_gn']
        user.last_name = meta['MELLON_sn']
        user.save()

user_logged_in.connect(configure_user)
