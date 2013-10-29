# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from auf.django.saml.settings import SAML_LOGOUT_REDIRECT_URL

from .middleware import LOGGED_USER_EMAIL
from .common import CommonTest


class DevTest(CommonTest):
    """
    Teste le comportement en mode sandbox.
    """

    def test_admin_index(self):
        """
        La page d'index affiche le form de login.
        """
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        location, dummy = self.redirectize(response['location']).split('?')
        self.assertEqual(location, reverse('sandbox_login'))

    def test_admin_login_no_user(self):
        """
        Le compte local n'est pas présent.
        """
        url = reverse('admin:index')
        response = self.client.get(url, follow=True)
        login_url, dummy = self.redirectize(
            response.redirect_chain[0][0]).split('?')
        response = self.client.post(login_url, {
            'username': LOGGED_USER_EMAIL,
            },
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucun utilisateur local.")

    def test_admin_login_user_in(self):
        """
        Le compte local est présent.
        """
        self.creer_user()
        url = reverse('admin:index')
        response = self.client.get(url, follow=True)
        login_url = self.redirectize(
            response.redirect_chain[0][0])
        response = self.client.post(login_url, {
            'username': LOGGED_USER_EMAIL,
            },
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(url, self.redirectize(response['location']))

    def test_admin_logout(self):
        """
        Déconnexion locale.
        """
        self.creer_user()
        url = reverse('admin:index')
        response = self.client.get(url, follow=True)
        login_url = self.redirectize(
            response.redirect_chain[0][0])
        self.client.post(login_url, {
            'username': LOGGED_USER_EMAIL,
            },
            )
        response = self.client.get(reverse('admin:logout'), follow=True)
        urls = [self.redirectize(u).split('?')[0] for (u, status_code) in
                response.redirect_chain]
        self.assertEqual(urls[0], reverse('local_logout'))
        self.assertEqual(urls[1], reverse('sandbox_logout'))
        self.assertEqual(urls[2], SAML_LOGOUT_REDIRECT_URL)
