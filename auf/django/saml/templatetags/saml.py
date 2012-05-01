# -*- coding: utf-8 -*-

from django import template
from auf.django.saml.views import redirect_to_login, redirect_to_logout

register = template.Library()

@register.simple_tag(takes_context=True)
def mellon_login_url(context, url=None):
    return redirect_to_login(context['request'], url, do_redirect=False)


@register.simple_tag(takes_context=True)
def mellon_logout_url(context, url=None):
    return redirect_to_logout(context['request'], url, do_redirect=False)
