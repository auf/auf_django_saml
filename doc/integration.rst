Intégration
***********

Cette partie explique comment bien construire les templates.

Ce paquet fourni des templatetags, pour ne pas avoir à réfléchir
aux urls utilisées pour les redirections au serveur d'identités
ou encore les urls en mode développement.

Voici un exemple de ce qu'on pourrait trouver dans une template
Django pour générer un **lien de connexion** ou un **lien de 
déconnexion** si le user est connecté ou non:

.. code-block:: guess

    {% load saml %}
    
    {% if request.user.is_authenticated %}
        {% mellon_logout_url %}
    {% else %}
        {% mellon_login_url request.get_full_path %}
