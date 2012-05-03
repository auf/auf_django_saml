# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from auf.django.references import models as ref


class Command(BaseCommand):
    """
    Outils concernant les comptes relatifs aux employes
    """
    def handle(self, *args, **options):
        if len(args) == 0:
            self.stdout.write('Commandes:\n')
            self.stdout.write('* import (ref_employes => django_user)\n')
            return

        if args[0] == 'import':
            nb_employes = 0
            for e in ref.Employe.objects.filter(actif=True):
                username = e.courriel.replace('@auf.org', '')
                django_user, created = \
                    User.objects.get_or_create(username=username)
                django_user.username = username
                django_user.first_name = e.prenom
                django_user.last_name = e.nom
                django_user.email = e.courriel
                django_user.save()
                nb_employes += 1
            self.stdout.write('%s employés ont été importés.\n' % nb_employes)
