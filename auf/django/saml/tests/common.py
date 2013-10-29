# -*- coding: utf-8 -*-

import urllib
import urlparse

from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User

from auf.django.references import models as ref

from .middleware import LOGGED_USER_EMAIL, ANONYMOUS_KEY, LOGGED_USER_USERNAME


class CommonTest(TestCase):

    def setUp(self):
        self.client = Client()

    def anonymize(self, url):
        """
        Ajoute un flag dans l'URL pour fonctionner comme utilisateur non
        authentifié.
        """
        params = {ANONYMOUS_KEY: 1, }
        url_parts = urlparse.urlsplit(url)
        qs = urlparse.parse_qs(url_parts[4])
        qs.update(params)
        return "%s?%s" % (url, urllib.urlencode(qs), )

    def redirectize(self, url):
        """
        Extrait de l'URL le protocole et fqdn
        """
        url_parts = urlparse.urlsplit(url)
        if url_parts[3]:
            return "%s?%s" % (url_parts[2], url_parts[3], )
        else:
            return url_parts[2]

    def creer_employe(self):
        """
        Créer un employé correspondant à la personne connecté dans le
        MockMiddleware.
        """
        ref.Employe(
            implantation_id=1,
            implantation_physique_id=1,
            service_id=1,
            courriel=LOGGED_USER_EMAIL).save()

    def creer_user(self):
        """
        Créer un user Django staff correspondant à la personne connecté dans le
        MockMiddleware.
        """
        User(
            is_staff=True,
            username=LOGGED_USER_USERNAME,
            email=LOGGED_USER_EMAIL).save()
