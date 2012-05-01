# -*- coding: utf-8 -*-


def is_employe(user):
    """
    La dépendance au paquet auf.django.references
    est condiotionnelle, on peut imaginer que l'application
    soit uniquement pour d'autres types de personnes.
    """
    try:
        from auf.django.references.models import Employe
    except:
        return False

    if not hasattr(user, 'email'):
        return False
    return Employe.objects.filter(courriel=user.email).exists()
