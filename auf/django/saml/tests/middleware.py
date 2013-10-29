# -*- coding: utf-8 -*-

ANONYMOUS_KEY = 'anonymous'

LOGGED_USER_EMAIL = 'admin@auf.org'
LOGGED_USER_USERNAME = LOGGED_USER_EMAIL.replace('@auf.org', '')
LOGGED_USER_GN = 'admin_gn'
LOGGED_USER_SN = 'admin_sn'


class MockMiddleware(object):
    """
    Fake auth sur notre IdP id.auf.org
    """
    def process_request(self, request):
        if not ANONYMOUS_KEY in request.META['QUERY_STRING']:
            request.META['REMOTE_USER'] = LOGGED_USER_EMAIL
            request.META['MELLON_mail'] = LOGGED_USER_EMAIL
            request.META['MELLON_gn'] = LOGGED_USER_GN
            request.META['MELLON_sn'] = LOGGED_USER_SN
