# -*- coding: utf-8 -*-
"""
Ce module définit toutes les constantes utilisées par le paquet 
auf.django.saml. Chacune peut être surchargée dans les settings
chargés par Django, typiquement le fichier project/conf.py.
"""
from django.conf import settings


# Active par défaut l'utilisation du serveur d'identités
SAML_AUTH = getattr(settings, 'SAML_AUTH', True)

# Variable utilisée pour fournir au serveur d'identités les
# adresses de retour du site.
SAML_REDIRECT_FIELD_NAME = getattr(settings, '', 'ReturnTo')

# URL de la page où l'utilisateur sera redirigé après déconnexion
SAML_LOGOUT_REDIRECT_URL = getattr(settings,'', '/')

# URL où est mappée la fonction login du module Apache Mellon
SAML_MELLON_LOGIN_URL = getattr(settings, '', '/mellon/login')

# URL où est mappée la fonction logout du module Apache Mellon
SAML_MELLON_LOGOUT_URL = getattr(settings, '', '/mellon/logout')

# URL où l'utilisateur peut modifier les propriétés globales de son profil 
SAML_CHANGE_PASSWORD_URL = getattr(settings, '', 'http://id.auf.org/profile')
