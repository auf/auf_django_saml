# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import Client


class CommonTest(TestCase):

    def setUp(self):
        self.client = Client()
