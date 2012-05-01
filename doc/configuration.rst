Configuration
*************

Cablâge de SAML dans le site
============================

Le paquet apporte :

  * de nouvelles urls

  * de nouveaux backends d'autentification

  * de nouveaux middlewares

qui doivent être déclarés dans le projet afin d'être effectivement utilisés.

Fichier *project/urls.py*
-------------------------

.. warning::

  Les urls de *auf.django.saml.urls* doit être déclarées avant celles des admins (*admin.sites.urls* ou *admin_tools.urls*)
  afin de cour-circuiter la page de connexion et de changement de mot de passe. 


.. code-block:: python

    from auf.django.saml import settings as saml_settings

    urlpatterns = patterns(
        '',
        ...
        (r'^', include('auf.django.saml.urls')),
        ...
        )

    if not saml_settings.SAML_AUTH:
        urlpatterns += patterns(
                '',
                (r'^', include('auf.django.saml.mellon_urls')),
        )

Fichier *project/settings.py*
-----------------------------

.. code-block:: python

    INSTALLED_APP = (
        ...
        'auf.djangl.saml',
        ...
    )

Fichier *project/conf.py*
-------------------------

.. Warning::
    Ce fichier est local, non commité, contenant des informations sensibles
    relative à l'environnement de déploiement.

.. Warning::
    En production, aucunes options SAML ne devraient être redéfinies
    
Ce paquet dispose d'une option utile en mode développement:

**SAML_AUTH** peut être positionné à **False**, ce que a pour effet de simuler la présence
du serveur d'identités en terme de passages entre les 2 sites.

.. code-block:: python

    SAML_AUTH = False


Fichier *project/settings.py*
-----------------------------

* Middleware **SMiddleware**

.. Warning::
    *auf.django.saml.middleware.SPMiddleware* doit impérativement être déclaré après
    *django.contrib.auth.middleware.AuthenticationMiddleware*.
    
.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'auf.django.saml.middleware.SPMiddleware',
        ...
        )

* Backend d'autentification **SPBackend**

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        'auf.django.saml.backends.SPBackend',
    )


Options
=======

.. literalinclude:: ../auf/django/saml/settings.py
