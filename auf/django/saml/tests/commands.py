# -*- coding: utf-8 -*-

from StringIO import StringIO

from django.contrib.auth.models import User

from auf.django.saml.management.commands.employes \
    import Command as EmployeCommand

from .middleware import LOGGED_USER_USERNAME, LOGGED_USER_EMAIL, \
    LOGGED_USER_GN, LOGGED_USER_SN
from .common import CommonTest


class CommandTest(CommonTest):
    """
    Teste les commandes Django.
    """
    def test_employe_aide(self):
        """
        Test aide
        """
        cmd = EmployeCommand()
        cmd.stdout = StringIO()
        cmd.handle()
        self.assertTrue("import" in cmd.stdout.getvalue())

    def test_employe_import(self):
        """
        Test l'import des employes
        """
        self.creer_employe()
        cmd = EmployeCommand()
        cmd.stdout = StringIO()
        cmd.handle('import')
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, LOGGED_USER_USERNAME,)
        self.assertEqual(users[0].email, LOGGED_USER_EMAIL,)
        self.assertEqual(users[0].first_name, LOGGED_USER_SN,)
        self.assertEqual(users[0].last_name, LOGGED_USER_GN,)

    def test_employe_import_fois2(self):
        """
        Test le multiple import
        """
        self.creer_employe()
        cmd = EmployeCommand()
        cmd.stdout = StringIO()
        cmd.handle('import')
        cmd.handle('import')
        users = User.objects.all()
        self.assertEqual(len(users), 1)

    def test_employe_import_sans_courriel(self):
        """
        Les employés sans courriel ne sont pas importés.
        """
        self.creer_employe_sans_courriel()
        cmd = EmployeCommand()
        cmd.stdout = StringIO()
        cmd.handle('import')
        users = User.objects.all()
        self.assertEqual(len(users), 0)
