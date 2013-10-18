# -*- coding: utf-8 -*-

from views import redirect_to_login, redirect_to_logout
from django.contrib.admin import site


def saml_login(request, extra_context=None):
    return redirect_to_login(request)


def saml_logout(request, extra_context=None):
    return redirect_to_logout(request)

# on recable runtime les fonctions qui prennent en charge
# l'authentification pour communiquer avec l'IdP
site.login = saml_login
site.logout = saml_logout
