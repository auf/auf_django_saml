# -*- coding: utf-8 -*-

import re

from django.core.urlresolvers import reverse

from auf.django.saml import settings

from .common import CommonTest


class TemplateTagTest(CommonTest):
    """
    Teste les fonctionnalités des templatetags SAML.
    """
    url = reverse('test_tags')

    def setUp(self):
        super(TemplateTagTest, self).setUp()
        self.url = reverse('test_tags')
        self.response = self.client.get(self.url)

    def test_templatetag_login_var(self):
        """
        Test le rendu du templatetag *mellon_login_url* avec une variable en
        paramètre.
        """
        regex = "test_templatetag_login_var:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        login_url, redirect_url = m.groups()
        self.assertEqual(login_url, settings.SAML_MELLON_LOGIN_URL)
        self.assertEqual(redirect_url, self.url)

    def test_templatetag_login_default(self):
        """
        Test le rendu du templatetag *mellon_login_url* sans paramètre.
        """
        regex = "test_templatetag_login_default:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        login_url, redirect_url = m.groups()
        self.assertEqual(login_url, settings.SAML_MELLON_LOGIN_URL)
        self.assertEqual(redirect_url, self.url)

    def test_templatetag_login_string(self):
        """
        Test le rendu du templatetag *mellon_login_url* avec paramètre string.
        """
        regex = "test_templatetag_login_string:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        login_url, redirect_url = m.groups()
        self.assertEqual(login_url, settings.SAML_MELLON_LOGIN_URL)
        self.assertEqual(redirect_url, '/admin')

    def test_templatetag_logout_var(self):
        """
        Test le rendu du templatetag *mellon_logout_url* avec une variable en
        paramètre.
        """
        regex = "test_templatetag_logout_var:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        logout_url, redirect_url = m.groups()
        self.assertEqual(logout_url, reverse('local_logout'))
        self.assertEqual(redirect_url, self.url)

    def test_templatetag_logout_default(self):
        """
        Test le rendu du templatetag *mellon_logout_url* sans paramètre.
        """
        regex = "test_templatetag_logout_default:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        logout_url, redirect_url = m.groups()
        self.assertEqual(logout_url, reverse('local_logout'))
        self.assertEqual(redirect_url, settings.SAML_LOGOUT_REDIRECT_URL)

    def test_templatetag_logout_string(self):
        """
        Test le rendu du templatetag *mellon_logout_url* avec paramètre string.
        """
        regex = "test_templatetag_logout_string:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        logout_url, redirect_url = m.groups()
        self.assertEqual(logout_url, reverse('local_logout'))
        self.assertEqual(redirect_url, '/admin')
