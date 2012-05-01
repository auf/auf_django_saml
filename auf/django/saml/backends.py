# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.backends import RemoteUserBackend, ModelBackend
from auf.django.saml import settings
    

class FakeSPBackend(ModelBackend):
    """
    On autentifie uniquement sur le username
    """
    def authenticate(self, username=None, password=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


class RealSPBackend(RemoteUserBackend):
    """
    Backend reposant sur le id.auf.org
    """
    create_unknown_user = True

    def clean_username(self, username):
        """
        Le IdP retourne le courriel
        """
        return username.replace('@auf.org', '')

if settings.SAML_AUTH:
    SPBackend = RealSPBackend
else:
    SPBackend = FakeSPBackend


