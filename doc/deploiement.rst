Déploiement
***********

Lorsqu'on parle de déploiement, c'est dans le sens où on désire brancher
son site Web avec Apache, Mellon et le serveur d'identités.

Cette opération peut se faire localement, sous réserve que notre application
soit déclarée sur le serveur d'autentification.

Prérequis
=========

Installer Apache >=2
++++++++++++++++++++


Installer Mellon
++++++++++++++++

.. warning::

    TODO : Demander à JC pour le dépôt AUF

.. warning::

    La version installée doit respecter ces versions:
    
    * mod_mellon >= 0.4
    
    * liblasso3 > 2.2.2

.. Note::

   Configurer Apache pour qu'il charge ce nouveau module dans le fichier
   */etc/apache/httpd.conf*

   LoadModule auth_mellon_module /usr/lib/apache2/modules/mod_auth_mellon.so


Créer un nouveau host
+++++++++++++++++++++

Ajout d'un host dans le fichier *etc/hosts*, exemple ici: **olarcheveque**


Créer les fichiers pour communiquer avec le serveur d'identités
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**metadata.xml**::

    wget --no-check-certificate https://id.auf.org/idp/saml2/metadata -O /srv/id.auf.org-metadata.xml

**clefs**::

    openssl req -new -x509 -keyout /srv/olarcheveque-mellon-key.pem -out /srv/olarcheveque-mellon-cert.pem -nodes -days 3650 -newkey rsa:2048 -subj "/CN=olarcheveque" 

Créer un vhost *olarcheveque*
+++++++++++++++++++++++++++++

dans /etc/site-available/olarcheveque:

::

  <VirtualHost *:80>
          ServerName olarcheveque
          ErrorLog /var/log/apache2/olarcheveque-error.log
          LogLevel warn
          CustomLog /var/log/apache2/olarcheveque-access.log combined
          Alias /static /net/nfs-authnss.b.ca.auf/home/olivier.larcheveque/Projets/olarcheveque/sitestatic
          WSGIScriptAliasMatch ^/(?!mellon) /net/nfs-authnss.b.ca.auf/home/olivier.larcheveque/Projets/olarcheveque/bin/django.wsgi
  
          <Location />
                  AuthType "Mellon" 
                  MellonEnable "info" 
                  MellonUser "mail" 
                  MellonOrganizationName "olarcheveque" 
                  MellonOrganizationDisplayName "fr" "olarcheveque" 
                  MellonOrganizationURL "http://www.auf.org" 
                  MellonSPPrivateKeyFile /srv/olarcheveque-mellon-key.pem
                  MellonSPCertFile /srv/olarcheveque-mellon-cert.pem
                  MellonIdPMetadataFile /srv/id.auf.org-metadata.xml
          </Location>
  
  </VirtualHost>

.. note::

  Ne pas oublier d'activer le vhost avec **a2ensite**.

Déboggage
=========

.. versionadded:: 1.1

    Les variables transférées par mellon peuvent être loggées
    pour fin d'examen.

Exemple de configuration de LOGGING dans *project/conf.py*::

    import os
    from django.conf.global_settings import LOGGING as DEFAULT_LOGGING

    PROJECT_ROOT = os.path.dirname(__file__)
    SITE_ROOT = os.path.dirname(PROJECT_ROOT)
    
    LOGGING = DEFAULT_LOGGING

    LOGGING['handlers']['file'] = {
        'level':'DEBUG',
        'class':'logging.FileHandler',
        'filename': os.path.join(SITE_ROOT, 'django.log'),
    }

    LOGGING['loggers']['SAML'] = {
        'handlers': ['file', ],
        'level': 'DEBUG',
        'propogate': False
        }

