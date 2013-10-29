# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from auf.django.saml import settings

from .middleware import LOGGED_USER_EMAIL, LOGGED_USER_GN, LOGGED_USER_SN
from .common import CommonTest


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
        self.creer_user()
        url = reverse('admin:index')
        self.client.get(url)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_logout(self):
        """
        Test la redirection du logout local puis au IdP
        """
        self.creer_user()
        url = reverse('admin:logout')
        response = self.client.get(url)
        location, qs = self.redirectize(response['location']).split('?')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(location, reverse('local_logout'))

        response = self.client.get(location)
        self.assertEqual(response.status_code, 302)

    def test_admin_change_password(self):
        """
        Test que le changement de mot de passe redirige vers l'IdP.
        """
        self.creer_user()
        url = reverse('admin:password_change')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
