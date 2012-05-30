Outils
******

Ce paquet apporte :

.. versionadded:: 1.0

.. warning::

    vous devez avoir le paquet *auf.django.references* d'installé.


* un décorateur **employe_required**::

    from auf.django.saml.decorators import employe_required

.. versionadded:: 1.2

.. warning::

    vous devez avoir le paquet *auf.django.references* d'installé.

* une commande Django pour prépopuler les employés **bin/django employes import**::

    bin/django employes import


.. versionadded:: 1.5


* un décorateur **login_required**::

    from auf.django.saml.decorators import login_required

*  une réponse HTTP pour **rediriger vers la page de login**::

    from auf.django.saml.views import redirect_to_login

