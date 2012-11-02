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
        info = u""
        for k, v in request.META.items():
            if k.startswith('MELLON') or k is 'REMOTE_USER':
                info += u"\n%s : %s" % (k, v)

        logger.info(info)
        if not saml_settings.SAML_AUTH:
            return

        return super(SPMiddleware, self).process_request(request)


def configure_user(sender, request, user, *args, **kwargs):
    """
    Au login, on synchronise les infos du serveur d'identités
    avec le user local
    """
    if saml_settings.SAML_AUTH:
        meta = request.META
        user.email = meta['MELLON_mail']
        user.first_name = meta['MELLON_gn']
        user.last_name = meta['MELLON_sn']
        user.save()
        logger.info(u"")

user_logged_in.connect(configure_user)
