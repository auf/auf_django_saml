# -*- coding: utf-8 -*-

from django import template
from auf.django.saml.views import redirect_to_login, redirect_to_logout

register = template.Library()


class UrlNode(template.Node):

    def __init__(self, fct, url):
        self.fct = fct
        self.url = url

    def render(self, context):
        return self.fct(context['request'], self.url, do_redirect=False)


def mellon_login_url(parser, token):
    try:
        tag_name, url, = token.split_contents()
    except:
        url = None
    return UrlNode(redirect_to_login, url)
register.tag('mellon_login_url', mellon_login_url)


def mellon_logout_url(parser, token):
    try:
        tag_name, url, = token.split_contents()
    except:
        url = None
    return UrlNode(redirect_to_logout, url)
register.tag('mellon_logout_url', mellon_logout_url)
