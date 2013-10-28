# -*- coding: utf-8 -*-

from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as _

from views import redirect_to_login
from permissions import is_employe
from settings import SAML_REDIRECT_FIELD_NAME


def employe_required(
        function=None,
        redirect_field_name=SAML_REDIRECT_FIELD_NAME,
        login_url=None):
    """
    Vérifie que le user connecté est bien un employé de l'AUF,
    autrement il est redirigé sur la page de connexion.
    """

    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request, redirect_to=login_url)
        if is_employe(request.user):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                _(u"Votre compte ne permet pas d'accéder à cette page"))

    return _wrapped_view


def login_required(
        function=None,
        redirect_field_name=SAML_REDIRECT_FIELD_NAME,
        login_url=None):
    """
    Vérifie que le user connecté est bien connecté,
    autrement il est redirigé sur la page de connexion.
    """

    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return function(request, *args, **kwargs)
        else:
            return redirect_to_login(request, redirect_to=login_url)
    return _wrapped_view
