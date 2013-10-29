# -*- coding: utf-8 -*-


def is_employe(user):
    """
    La dépendance au paquet auf.django.references
    est conditionnelle, on peut imaginer que l'application
    soit uniquement pour d'autres types de personnes.
    """
    from auf.django.references.models import Employe
    return Employe.objects.filter(courriel=user.email).exists()
