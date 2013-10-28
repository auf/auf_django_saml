# -*- coding: utf-8 -*-

import re
import urllib

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from auf.django.saml import settings
from auf.django.references import models as ref

from .middleware import LOGGED_USER_EMAIL, LOGGED_USER_GN, LOGGED_USER_SN
from .common import CommonTest


class PermissionTest(CommonTest):
    """
    Teste les outils de sécurisation.
    """

    def test_employe_required_anonymous(self):
        """
        Test le decorateur sans utilisateur connecté.
        """
        url = self.anonymize(reverse('test_employe_required'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_employe_required_authenticated(self):
        """
        Test le decorateur avec un utilisateur connecté.
        """
        url = reverse('test_employe_required')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_employe_required_ok(self):
        """
        Test le decorateur avec un employé connecté.
        """
        ref.Employe(
            courriel=LOGGED_USER_EMAIL).save()
        url = reverse('test_employe_required')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        """
        Test le décorateur de connexion requise.
        """
        url = self.anonymize(reverse('test_login_required'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class AdminTest(CommonTest):
    """
    Teste le comportement de l'admin avec l'IDP.
    """

    def test_anonymize(self):
        """
        Test la fonction qui ajoute un params GET.
        """
        url = self.anonymize(reverse('admin:index'))
        self.assertEqual(url.count('?'), 1)

    def test_admin_index_anonymous(self):
        """
        La page de login de l'admin doît être désactivée.
        Il n'y a pas de redirection vers le login.
        """
        url = self.anonymize(reverse('admin:index'))
        response = self.client.get(url)
        self.assertEqual(
            response['location'].count('?'),
            1,
            response['location'])
        self.assertEqual(response.status_code, 302)
        location, dummy = self.redirectize(response['location']).split('?')
        self.assertEqual(location, settings.SAML_MELLON_LOGIN_URL)

    def test_admin_index_authenticated(self):
        """
        L'admin est inacessible par défaut, mais le user est crée à la volée.
        """
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(User.objects.count(), 1)
        user = User.objects.all()[0]
        email = LOGGED_USER_EMAIL.replace('@auf.org', '')
        self.assertEqual(user.username, email,)
        self.assertEqual(user.email, LOGGED_USER_EMAIL,)
        self.assertEqual(user.first_name, LOGGED_USER_GN)
        self.assertEqual(user.last_name, LOGGED_USER_SN)

    def test_admin_login(self):
        """
        Test l'accès à l'admin selon le flag is_staff du compte local.
        """
        url = reverse('admin:index')
        self.client.get(url)
        user = User.objects.all()[0]
        user.is_staff = True
        user.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_logout(self):
        """
        Test la redirection du logout local puis au IdP
        """
        url = reverse('admin:index')
        self.client.get(url)
        user = User.objects.all()[0]
        user.is_staff = True
        user.save()

        url = reverse('admin:logout')
        response = self.client.get(url)
        location, qs = self.redirectize(response['location']).split('?')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(location, reverse('local_logout'))


class TemplateTagTest(CommonTest):
    """
    Teste les fonctionnalités des templatetags SAML.
    """

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
        self.assertEqual(redirect_url, urllib.quote_plus(self.url))

    def test_templatetag_login_default(self):
        """
        Test le rendu du templatetag *mellon_login_url* sans paramètre.
        """
        regex = "test_templatetag_login_default:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        login_url, redirect_url = m.groups()
        self.assertEqual(login_url, settings.SAML_MELLON_LOGIN_URL)
        self.assertEqual(redirect_url, urllib.quote_plus(self.url))

    def test_templatetag_login_string(self):
        """
        Test le rendu du templatetag *mellon_login_url* avec paramètre string.
        """
        regex = "test_templatetag_login_string:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        login_url, redirect_url = m.groups()
        self.assertEqual(login_url, settings.SAML_MELLON_LOGIN_URL)
        self.assertEqual(redirect_url, urllib.quote_plus('/admin'))

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
        self.assertEqual(redirect_url, urllib.quote_plus(self.url))

    def test_templatetag_logout_default(self):
        """
        Test le rendu du templatetag *mellon_logout_url* sans paramètre.
        """
        regex = "test_templatetag_logout_default:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        logout_url, redirect_url = m.groups()
        self.assertEqual(logout_url, reverse('local_logout'))
        self.assertEqual(
            redirect_url,
            urllib.quote_plus(settings.SAML_LOGOUT_REDIRECT_URL))

    def test_templatetag_logout_string(self):
        """
        Test le rendu du templatetag *mellon_logout_url* avec paramètre string.
        """
        regex = "test_templatetag_logout_string:(.*)\?%s=(.*)\n" % (
            settings.SAML_REDIRECT_FIELD_NAME, )
        m = re.search(regex, self.response.content)
        logout_url, redirect_url = m.groups()
        self.assertEqual(logout_url, reverse('local_logout'))
        self.assertEqual(redirect_url, urllib.quote_plus('/admin'))
