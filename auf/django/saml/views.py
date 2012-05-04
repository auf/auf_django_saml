# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from forms import RemoteUserForm
from settings import SAML_REDIRECT_FIELD_NAME,\
        SAML_MELLON_LOGIN_URL,\
        SAML_MELLON_LOGOUT_URL,\
        SAML_CHANGE_PASSWORD_URL,\
        SAML_LOGOUT_REDIRECT_URL, \
        SAML_AUTH


def redirect_to_login(request, redirect_to=None, do_redirect=True):
    if redirect_to is None:
        redirect_to = request.get_full_path()
    if SAML_AUTH:
        base_url = SAML_MELLON_LOGIN_URL
    else:
        base_url = reverse('sandbox_login')
    url = "%s?%s=%s" % (base_url,
            SAML_REDIRECT_FIELD_NAME,
            redirect_to,
            )
    if do_redirect:
        return redirect(url)
    else:
        return url


def redirect_to_logout(request, redirect_to=None, do_redirect=True):
    if redirect_to is None:
        redirect_to = SAML_LOGOUT_REDIRECT_URL
    url = "%s?%s=%s" % (reverse('local_logout'),
            SAML_REDIRECT_FIELD_NAME,
            redirect_to,
            )
    if do_redirect:
        return redirect(url)
    else:
        return url


def login_form(request, ):
    """
    Page de login en mode développement
    permet de se connecter avec un user selon son username défini localemement
    """
    redirect_to = request.REQUEST.get(SAML_REDIRECT_FIELD_NAME, '/')
    if request.method == "POST":
        form = RemoteUserForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect(redirect_to)
    else:
        form = RemoteUserForm(request)

    c = {'form': form}
    return render_to_response("saml/login_form.html",
        c,
        context_instance=RequestContext(request))


def local_logout(request, ):
    """
    Logout pour SAML pour détruire la session Django
    """
    query_string = request.META['QUERY_STRING']
    auth_logout(request)
    if SAML_AUTH:
        base_url = SAML_MELLON_LOGOUT_URL
    else:
        base_url = reverse('sandbox_logout')
    logout_url = "%s?%s" % (base_url, query_string)
    response = HttpResponse(content="", status=303)
    response["Location"] = logout_url
    return response


def mellon_logout(request, ):
    """
    Simule la vue qui de mellon qui initie le logout sur le l'IdP
    """
    redirect_to = request.REQUEST.get(SAML_REDIRECT_FIELD_NAME, '/')
    return redirect(redirect_to)


def password_change(request, ):
    return redirect(SAML_CHANGE_PASSWORD_URL)
