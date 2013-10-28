# -*- coding: utf-8 -*-

import urllib
import urlparse

from django.test import TestCase
from django.test.client import Client

from .middleware import ANONYMOUS_KEY


class CommonTest(TestCase):

    def setUp(self):
        self.client = Client()

    def anonymize(self, url):
        params = {ANONYMOUS_KEY: 1, }
        url_parts = urlparse.urlsplit(url)
        qs = urlparse.parse_qs(url_parts[4])
        qs.update(params)
        return "%s?%s" % (url, urllib.urlencode(qs), )

    def redirectize(self, url):
        url_parts = urlparse.urlsplit(url)
        return "%s?%s" % (url_parts[2], url_parts[3], )
