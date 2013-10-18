# -*- coding: utf-8 -*-

from django import template

from auf.django.saml.views import redirect_to_login, redirect_to_logout

register = template.Library()


@register.simple_tag(takes_context=True, name='mellon_login_url')
def mellon_login_url(context, url=None):
    request = context['request']
    return redirect_to_login(request, redirect_to=url, do_redirect=False)


@register.simple_tag(takes_context=True, name='mellon_logout_url')
def mellon_logout_url(context, url=None):
    request = context['request']
    return redirect_to_logout(request, redirect_to=url, do_redirect=False)
