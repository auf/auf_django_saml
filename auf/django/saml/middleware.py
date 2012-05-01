# -*- coding: utf-8 -*-

from django.contrib.auth.middleware import RemoteUserMiddleware
from auf.django.saml import settings

class SPMiddleware(RemoteUserMiddleware):

    def process_request(self, request):
        if not settings.SAML_AUTH:
            return
        return super(SPMiddleware, self).process_request(request)
