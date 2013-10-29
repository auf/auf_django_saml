# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

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
        self.creer_employe()
        url = reverse('test_employe_required')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_required_anonymous(self):
        """
        Test le décorateur de connexion requise avec un anonyme.
        """
        url = self.anonymize(reverse('test_login_required'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_login_required_authenticated(self):
        """
        Test le décorateur de connexion requise.
        """
        url = reverse('test_login_required')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
